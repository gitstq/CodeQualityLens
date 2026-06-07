"""
Setup script for CodeQualityLens.
"""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="codequalitylens",
    version="1.0.0",
    author="CodeQualityLens Team",
    author_email="codequalitylens@example.com",
    description="🔍 Lightweight AI-Generated Code Quality Detection Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/CodeQualityLens",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "codequalitylens=codequalitylens.cli:main",
            "cql=codequalitylens.cli:main",
        ],
    },
    keywords="code-quality static-analysis ai-generated-code security linting",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/CodeQualityLens/issues",
        "Source": "https://github.com/gitstq/CodeQualityLens",
    },
)
