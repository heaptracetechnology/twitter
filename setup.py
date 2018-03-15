#!/usr/bin/env python
import io
import os
import sys

from setuptools import find_packages, setup


setup(
    name='asyncy-twitter',
    description='Twitter container for Asyncy',
    author='Asyncy',
    author_email='noreply@asyncy.com',
    version='0.1.0',
    packages=find_packages(),
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-mock'
    ],
    setup_requires=['pytest-runner'],
    install_requires=[
        'click>=6.7',
        'tweepy>=3.6',
    ],
    entry_points="""
        [console_scripts]
        twitter=twitter.Cli:Cli.main
    """
)
