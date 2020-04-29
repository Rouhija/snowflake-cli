from setuptools import setup, find_packages

import os
import sys

py_version = sys.version_info[:2]
if not (3, 5) < py_version < (3, 9):
    raise RuntimeError('snowflake-cli needs Python version 3.6 - 3.8 to run')


with open("README.md", "r") as f:
    long_description = f.read()

dist = setup(
    name='snowflake-cli',
    version='1.0.0',
	url='https://github.com/Rouhija/snowflake-cli',
	description="A cli tool for automating tasks in Snowflake Database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sami Rouhe",
    author_email="rouhesami@gmail.com",
	packages=find_packages(),
    # test_suite="taskmaster.tests",
    entry_points={
        'console_scripts': [
			'snowflake-cli = srcs.snowflakectl:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
     ],
)