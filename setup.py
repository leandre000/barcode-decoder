"""
Setup script for Barcode Decoder
    # Commit 42: 2025-11-25 12:13:00
    # Commit 1: 2025-11-25 12:12:48
"""
from setuptools import setup, find_packages
    # Commit 6: 2025-11-25 12:12:49

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    # Commit 52: 2025-11-25 12:13:04

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="barcode-decoder",
    version="1.0.0",
    author="Leandre",
    author_email="",
    description="Professional barcode decoder with Aztec and Data Matrix support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leandre000/barcode-decoder",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "barcode-decoder=run:main",
        ],
    },
)

