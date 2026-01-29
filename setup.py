"""
Setup configuration for agora-rest-client-python package
"""
from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="agora-rest-client-python",
    version="0.1.0",
    author="Agora",
    author_email="support@agora.io",
    description="Python client for Agora REST APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/agora-rest-client-python",
    packages=find_packages(exclude=["examples", "tests"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    keywords=["agora", "rest", "api", "conversational-ai", "agent"],
    project_urls={
        "Homepage": "https://github.com/your-org/agora-rest-client-python",
        "Documentation": "https://github.com/your-org/agora-rest-client-python",
        "Repository": "https://github.com/your-org/agora-rest-client-python",
        "Bug Tracker": "https://github.com/your-org/agora-rest-client-python/issues",
    },
)
