#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import setup

version = '1.0'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh: 
     install_requires = fh.read().splitlines()


setup(name='hundlab-AFAT',
    package_dir={'':'src'},
    packages=['AFAT'],
    scripts=['src/AutomatedFibrosisAnalysisToolkit.py'],
    version=version,
    description='Automated Fibrosis Analysis Toolkit: A tool to quantify the amount of fibrosis in Masson’s Trichrome stains',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hundlab/MAT",
    author='Thomas Hund',
    author_email='hund.1@osu.edu',
    license='MIT',
    install_requires=install_requires,
    include_package_data=True,
    )

