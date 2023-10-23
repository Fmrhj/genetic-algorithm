# read the contents of your README file
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="generic-algorithm-light",
    version="0.1.1",
    description="A lightweight genetic algorithm package for optimization",
    author="Fernando Zepeda",
    author_email="fernando.zepeda@pm.me",
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
