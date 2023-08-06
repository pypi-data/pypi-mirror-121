#!/usr/bin/env python3

import databento
from setuptools import find_packages, setup


setup(
    name="databento",
    version=databento.__version__,
    description="Python client library for the Databento API",
    long_description="file: README.md",
    author="Databento",
    author_email="support@databento.com",
    url="https://github.com/databento/databento-python",
    license="MIT",
    keywords="databento financial market data API",
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    install_requires=[
        "aiofiles>=0.6.0",
        "aiohttp>=3.7.4",
        "numpy>=1.20.1",
        "pandas>=1.2.4",
        "requests>=2.25.1",
        "zstd>=1.4.5",
    ],
    python_requires=">=3.6.*",
    project_urls={
        "Bug Tracker": "https://github.com/databento/databento-python/issues",
        "Documentation": "https://docs.databento.com/reference-historical",
        "Source Code": "https://github.com/databento/databento-python",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
