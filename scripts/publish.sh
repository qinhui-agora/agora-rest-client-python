#!/bin/bash
# Quick publish script for agora-rest-client-python

set -e  # Exit on error

echo "🚀 Agora REST Client Python - Publishing Script"
echo "================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: setup.py not found. Please run this script from the project root."
    exit 1
fi

# Get version from setup.py
VERSION=$(python -c "import re; content=open('setup.py').read(); print(re.search(r'version=\"([^\"]+)\"', content).group(1))")
echo "📦 Package version: $VERSION"
echo ""

# Ask for confirmation
read -p "❓ Publish version $VERSION to PyPI? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Publishing cancelled."
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/
echo "✓ Cleaned"
echo ""

# Build the package
echo "🔨 Building package..."
python -m build
if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi
echo "✓ Build successful"
echo ""

# Check the distribution
echo "🔍 Checking distribution..."
python -m twine check dist/*
if [ $? -ne 0 ]; then
    echo "❌ Distribution check failed!"
    exit 1
fi
echo "✓ Distribution check passed"
echo ""

# Ask which repository to upload to
echo "📤 Upload destination:"
echo "  1) Test PyPI (recommended for first time)"
echo "  2) Production PyPI"
read -p "Choose (1/2): " -n 1 -r REPO_CHOICE
echo ""

if [[ $REPO_CHOICE == "1" ]]; then
    echo "📤 Uploading to Test PyPI..."
    python -m twine upload --repository testpypi dist/*
    echo ""
    echo "✅ Published to Test PyPI!"
    echo ""
    echo "📥 Test installation with:"
    echo "   pip install --index-url https://test.pypi.org/simple/ agora-rest-client-python"
    echo ""
    echo "🔗 View at: https://test.pypi.org/project/agora-rest-client-python/"
elif [[ $REPO_CHOICE == "2" ]]; then
    echo "📤 Uploading to Production PyPI..."
    python -m twine upload dist/*
    echo ""
    echo "✅ Published to PyPI!"
    echo ""
    echo "📥 Install with:"
    echo "   pip install agora-rest-client-python"
    echo ""
    echo "🔗 View at: https://pypi.org/project/agora-rest-client-python/"
else
    echo "❌ Invalid choice. Cancelled."
    exit 1
fi

echo ""
echo "🎉 Publishing complete!"
