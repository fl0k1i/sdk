"""
Setup configuration for Grep SDK

This file tells pip how to install the grep-sdk package.
"""

from setuptools import setup, find_packages
import os

# Read README for long description
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Grep SDK - LLM Observability Platform"

setup(
    # Package metadata
    name="grep-sdk",
    version="0.1.0",
    author="Grep Team",
    author_email="support@grep.com",  # Update with your email
    description="LLM Observability SDK for Grep Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/grep-sdk",  # Update with your repo
    
    # Package discovery
    packages=find_packages(),
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=[
        "traceloop-sdk>=0.49.2",
        "opentelemetry-api>=1.20.0",
        "opentelemetry-sdk>=1.20.0",
    ],
    
    # Optional dependencies (for development)
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    
    # PyPI classifiers
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
    
    # Keywords for PyPI search
    keywords="llm observability tracing monitoring ai ml openai anthropic grep",
    
    # Entry points (if you want CLI tools later)
    entry_points={
        "console_scripts": [
            # "grep-cli=grep.cli:main",  # Uncomment if you add CLI
        ],
    },
)
