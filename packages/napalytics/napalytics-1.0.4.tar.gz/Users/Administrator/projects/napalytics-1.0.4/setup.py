import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="napalytics",
    version="1.0.0",
    description="A Python test framework for data testing across multiple data sources",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ert068001/napalytics",
    author="Bryan",
    author_email="info@bryan.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["napalytics"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "napalytics=napalytics.__main__:main",
        ]
    },
)
