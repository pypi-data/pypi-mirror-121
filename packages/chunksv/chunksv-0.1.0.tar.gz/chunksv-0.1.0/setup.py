from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="chunksv",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    license="MIT",
    url="https://github.com/bengetch/chunksv",
    author="bengetch",
    author_email="bengetch@gmail.com",
    description="Python module for processing csv files in chunks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    test_suite="test"
)
