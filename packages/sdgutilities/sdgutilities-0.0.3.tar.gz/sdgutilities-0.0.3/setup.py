import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sdgutilities",
    version="0.0.3",
    author="UNSD",
    author_email="mark.iliffe@un.org",
    description="A library that provides a set of utilities for managing and analysing SDG data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/markiliffe/SDGUtilities",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)