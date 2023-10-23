#!/bin/bash

# Clean up the previous build and distribution files
rm -rf dist
rm -rf build

# Create a source distribution and a wheel distribution
python setup.py sdist bdist_wheel

# Check if the distribution was built successfully
if [ $? -ne 0 ]; then
    echo "Distribution build failed."
    exit 1
fi

# Upload the distribution to PyPI using twine
twine upload dist/*

# Clean up the build and distribution files
rm -rf dist
rm -rf build

echo "Package $PACKAGE_NAME version $PACKAGE_VERSION has been successfully pushed to PyPI."