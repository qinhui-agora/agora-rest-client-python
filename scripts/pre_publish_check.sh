#!/bin/bash
# Pre-publish checklist for agora-rest-client-python

set -e

echo "✅ Pre-Publish Checklist"
echo "========================"
echo ""

ERRORS=0

# Check 1: setup.py exists and is valid
echo "1️⃣  Checking setup.py..."
if [ ! -f "setup.py" ]; then
    echo "   ❌ setup.py not found"
    ERRORS=$((ERRORS + 1))
else
    python setup.py --version > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        VERSION=$(python setup.py --version)
        echo "   ✓ setup.py is valid (version: $VERSION)"
    else
        echo "   ❌ setup.py has errors"
        ERRORS=$((ERRORS + 1))
    fi
fi
echo ""

# Check 2: README.md exists
echo "2️⃣  Checking README.md..."
if [ ! -f "README.md" ]; then
    echo "   ❌ README.md not found"
    ERRORS=$((ERRORS + 1))
else
    echo "   ✓ README.md exists"
fi
echo ""

# Check 3: LICENSE exists
echo "3️⃣  Checking LICENSE..."
if [ ! -f "LICENSE" ]; then
    echo "   ⚠️  LICENSE not found (optional but recommended)"
else
    echo "   ✓ LICENSE exists"
fi
echo ""

# Check 4: requirements.txt exists
echo "4️⃣  Checking requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    echo "   ❌ requirements.txt not found"
    ERRORS=$((ERRORS + 1))
else
    echo "   ✓ requirements.txt exists"
fi
echo ""

# Check 5: Package structure
echo "5️⃣  Checking package structure..."
if [ ! -d "agora_rest" ]; then
    echo "   ❌ agora_rest/ directory not found"
    ERRORS=$((ERRORS + 1))
elif [ ! -f "agora_rest/__init__.py" ]; then
    echo "   ❌ agora_rest/__init__.py not found"
    ERRORS=$((ERRORS + 1))
else
    echo "   ✓ Package structure is correct"
fi
echo ""

# Check 6: Version in __init__.py matches setup.py
echo "6️⃣  Checking version consistency..."
SETUP_VERSION=$(python -c "import re; content=open('setup.py').read(); print(re.search(r'version=\"([^\"]+)\"', content).group(1))")
INIT_VERSION=$(python -c "import re; content=open('agora_rest/__init__.py').read(); print(re.search(r'__version__\s*=\s*\"([^\"]+)\"', content).group(1))")

if [ "$SETUP_VERSION" != "$INIT_VERSION" ]; then
    echo "   ❌ Version mismatch: setup.py ($SETUP_VERSION) != __init__.py ($INIT_VERSION)"
    ERRORS=$((ERRORS + 1))
else
    echo "   ✓ Version is consistent: $SETUP_VERSION"
fi
echo ""

# Check 7: Build tools installed
echo "7️⃣  Checking build tools..."
if ! command -v python &> /dev/null; then
    echo "   ❌ Python not found"
    ERRORS=$((ERRORS + 1))
else
    echo "   ✓ Python is installed"
fi

if ! python -c "import build" 2>/dev/null; then
    echo "   ⚠️  'build' package not installed (run: pip install build)"
else
    echo "   ✓ 'build' package is installed"
fi

if ! python -c "import twine" 2>/dev/null; then
    echo "   ⚠️  'twine' package not installed (run: pip install twine)"
else
    echo "   ✓ 'twine' package is installed"
fi
echo ""

# Check 8: Test import
echo "8️⃣  Testing package import..."
python -c "from agora_rest import AgentClient, ConvoAIClient; from agora_rest.agent import DeepgramASRConfig, OpenAILLMConfig, ElevenLabsTTSConfig" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ Package imports successfully"
else
    echo "   ❌ Package import failed"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 9: Examples exist
echo "9️⃣  Checking examples..."
if [ ! -d "examples" ]; then
    echo "   ⚠️  examples/ directory not found"
elif [ ! -f "examples/README.md" ]; then
    echo "   ⚠️  examples/README.md not found"
else
    echo "   ✓ Examples directory exists"
fi
echo ""

# Summary
echo "========================"
if [ $ERRORS -eq 0 ]; then
    echo "✅ All checks passed! Ready to publish."
    echo ""
    echo "Next steps:"
    echo "  1. Review PUBLISHING.md for detailed instructions"
    echo "  2. Run: ./scripts/publish.sh"
    exit 0
else
    echo "❌ $ERRORS error(s) found. Please fix before publishing."
    exit 1
fi
