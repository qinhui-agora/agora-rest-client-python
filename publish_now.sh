#!/bin/bash
# Interactive publishing script for agora-rest-client-python

set -e

echo "🚀 Agora REST Client Python - Publishing to PyPI"
echo "=================================================="
echo ""
echo "Version: 0.1.0"
echo ""

# Check if dist files exist
if [ ! -f "dist/agora_rest_client_python-0.1.0.tar.gz" ] || [ ! -f "dist/agora_rest_client_python-0.1.0-py3-none-any.whl" ]; then
    echo "❌ Distribution files not found in dist/"
    echo "   Please run: python -m build"
    exit 1
fi

echo "✅ Distribution files ready:"
ls -lh dist/
echo ""

# Ask which PyPI to use
echo "📤 Where do you want to publish?"
echo "   1) Test PyPI (https://test.pypi.org) - Recommended for first time"
echo "   2) Production PyPI (https://pypi.org)"
echo ""
read -p "Choose (1 or 2): " choice

if [ "$choice" = "1" ]; then
    REPO="testpypi"
    REPO_URL="https://test.pypi.org/legacy/"
    INSTALL_CMD="pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ agora-rest-client-python"
    VIEW_URL="https://test.pypi.org/project/agora-rest-client-python/"
elif [ "$choice" = "2" ]; then
    REPO="pypi"
    REPO_URL="https://upload.pypi.org/legacy/"
    INSTALL_CMD="pip install agora-rest-client-python"
    VIEW_URL="https://pypi.org/project/agora-rest-client-python/"
else
    echo "❌ Invalid choice"
    exit 1
fi

echo ""
echo "📝 You will need:"
echo "   - Username: __token__"
echo "   - Password: Your $REPO API token (starts with 'pypi-')"
echo ""
echo "   Get your token at:"
if [ "$choice" = "1" ]; then
    echo "   https://test.pypi.org/manage/account/token/"
else
    echo "   https://pypi.org/manage/account/token/"
fi
echo ""
read -p "Press Enter when ready to upload..."

echo ""
echo "📤 Uploading to $REPO..."
echo ""

# Upload
python -m twine upload --repository $REPO dist/*

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully published to $REPO!"
    echo ""
    echo "📥 Install with:"
    echo "   $INSTALL_CMD"
    echo ""
    echo "🔗 View at:"
    echo "   $VIEW_URL"
    echo ""
    echo "🎉 Done!"
else
    echo ""
    echo "❌ Upload failed. Please check the error message above."
    exit 1
fi
