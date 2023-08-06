import setuptools
from pathlib import Path

setuptools.setup(
    name="maiohhpdf",
    version=1.0,
    long_dercription=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
