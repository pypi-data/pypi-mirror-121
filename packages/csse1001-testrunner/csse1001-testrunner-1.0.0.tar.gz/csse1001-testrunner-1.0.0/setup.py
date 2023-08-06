import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="csse1001-testrunner",
    version="1.0.0",
    description="Testrunner used for testing in CSSE1001",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/CSSE1001/testrunner",
    author="CSSE1001",
    author_email="no-reply@uq.edu.au",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["testrunner"],
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.8",
)
