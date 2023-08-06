#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name='uravo',
    packages=find_packages(include=['uravo']),
    version='0.0.1',
    description='Python interface to the Uravo monitoring system',
    author='Patrick Gillan',
    author_email = 'pgillan@minorimpact.com',
    license='GPLv3',
    install_requires=['mysqlclient'],
    setup_requires=[],
    tests_require=[],
)
