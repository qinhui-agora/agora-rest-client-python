# Publishing Guide

This guide explains how to publish the `agora-rest-client-python` package to PyPI.

## Prerequisites

1. **PyPI Account**
   - Create an account at https://pypi.org/account/register/
   - Create an account at https://test.pypi.org/account/register/ (for testing)

2. **Install Build Tools**
   ```bash
   pip install --upgrade pip
   pip install --upgrade build twine
   ```

3. **API Token** (Recommended)
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token with scope for this project
   - Save the token securely (you'll only see it once)

## Pre-Release Checklist

Before publishing, ensure:

- [ ] All tests pass
- [ ] Version number is updated in `setup.py`
- [ ] `CHANGELOG.md` is updated with release notes
- [ ] `README.md` is up to date
- [ ] All examples work correctly
- [ ] Documentation is complete
- [ ] GitHub repository URL is correct in `setup.py`

## Step-by-Step Publishing Process

### 1. Update Version Number

Edit `setup.py` and update the version:

```python
version="0.1.0",  # Change this to your new version
```

Follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes

### 2. Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info/
```

### 3. Build the Package

```bash
# Build source distribution and wheel
python -m build
```

This creates:
- `dist/agora-rest-client-python-X.Y.Z.tar.gz` (source distribution)
- `dist/agora_rest_client_python-X.Y.Z-py3-none-any.whl` (wheel)

### 4. Test the Build Locally

```bash
# Install locally to test
pip install dist/agora_rest_client_python-X.Y.Z-py3-none-any.whl

# Test import
python -c "from agora_rest import AgentClient, ConvoAIClient; from agora_rest.agent import DeepgramASRConfig, OpenAILLMConfig, ElevenLabsTTSConfig; print('Import successful!')"

# Run examples
python examples/high_level_api/basic_usage.py
```

### 5. Upload to Test PyPI (Optional but Recommended)

```bash
# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*
```

When prompted:
- Username: `__token__`
- Password: Your Test PyPI API token (starts with `pypi-`)

Test installation from Test PyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ agora-rest-client-python
```

### 6. Upload to Production PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: Your PyPI API token (starts with `pypi-`)

### 7. Verify Publication

```bash
# Install from PyPI
pip install agora-rest-client-python

# Verify version
python -c "import agora_rest; print(agora_rest.__version__)"
```

Check the package page: https://pypi.org/project/agora-rest-client-python/

### 8. Create GitHub Release

1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag version: `v0.1.0` (match your package version)
4. Release title: `v0.1.0 - Initial Release`
5. Description: Copy from `CHANGELOG.md`
6. Attach the distribution files from `dist/`
7. Publish release

## Using API Tokens (Recommended)

Instead of entering credentials each time, configure `.pypirc`:

```bash
# Create/edit ~/.pypirc
cat > ~/.pypirc << EOF
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PYPI_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_PYPI_TOKEN_HERE
EOF

# Secure the file
chmod 600 ~/.pypirc
```

Then upload without prompts:
```bash
python -m twine upload dist/*
```

## Automated Publishing with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: python -m twine upload dist/*
```

Add your PyPI token to GitHub Secrets:
1. Go to repository Settings → Secrets → Actions
2. Add new secret: `PYPI_API_TOKEN`
3. Paste your PyPI API token

## Troubleshooting

### Error: "File already exists"
- You cannot re-upload the same version
- Increment the version number in `setup.py`
- Clean and rebuild: `rm -rf dist/ && python -m build`

### Error: "Invalid distribution"
- Check `setup.py` for syntax errors
- Ensure `README.md` exists and is valid Markdown
- Verify all required files are included in `MANIFEST.in`

### Error: "Authentication failed"
- Verify your API token is correct
- Ensure username is `__token__` (not your PyPI username)
- Check token has correct permissions

### Import errors after installation
- Check package structure: `agora_rest/__init__.py` must exist
- Verify `find_packages()` in `setup.py` finds all modules
- Test with: `python -c "import agora_rest; print(dir(agora_rest))"`

## Version History

Keep track of published versions:

| Version | Date | Notes |
|---------|------|-------|
| 0.1.0 | TBD | Initial release with join/leave APIs |

## Quick Reference

```bash
# Complete publishing workflow
rm -rf build/ dist/ *.egg-info/
python -m build
python -m twine check dist/*
python -m twine upload --repository testpypi dist/*  # Test first
python -m twine upload dist/*  # Production
```

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Semantic Versioning](https://semver.org/)
