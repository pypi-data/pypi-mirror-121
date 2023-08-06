from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'data analysis and statictic tools'
with open('README.md') as readme_file:
    LONG_DESCRIPTION = readme_file.read()
    

# Setting up
setup(
    name="jtatisctic",
    version=VERSION,
    author="Javad Salman",
    author_email="aetimpani@yandex.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url = 'https://github.com/cavadsalman/jtatistic',
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