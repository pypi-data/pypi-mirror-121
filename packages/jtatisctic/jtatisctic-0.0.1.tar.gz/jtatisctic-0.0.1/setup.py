from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'data analysis and statictic tools'
LONG_DESCRIPTION = 'jtatistic is a Python module for solving problems relevant to statistic topics.'

# Setting up
setup(
    name="jtatisctic",
    version=VERSION,
    author="Javad Salman",
    author_email="aetimpani@yandex.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'statistic', 'dataset'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)