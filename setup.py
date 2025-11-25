"""
    # Commit 140: 2025-11-25 12:13:34
    # Commit 129: 2025-11-25 12:13:30
Setup script for Barcode Decoder
    # Commit 94: 2025-11-25 12:13:19
    # Commit 42: 2025-11-25 12:13:00
    # Commit 128: 2025-11-25 12:13:30
    # Commit 67: 2025-11-25 12:13:09
    # Commit 1: 2025-11-25 12:12:48
"""
from setuptools import setup, find_packages
    # Commit 123: 2025-11-25 12:13:28
    # Commit 64: 2025-11-25 12:13:08
    # Commit 6: 2025-11-25 12:12:49
    # Commit 109: 2025-11-25 12:13:24

    # Commit 85: 2025-11-25 12:13:16
    # Commit 77: 2025-11-25 12:13:13
with open("README.md", "r", encoding="utf-8") as fh:
    # Commit 65: 2025-11-25 12:13:08
    # Commit 56: 2025-11-25 12:13:05
    # Commit 62: 2025-11-25 12:13:07
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

