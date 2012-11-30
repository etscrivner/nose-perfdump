#!/usr/bin/env python

from setuptools import setup, find_packages


version = '1.1'


long_desc = """
nose-perfdump is a Nose plugin that collects per-test performance metrics into an
SQLite3 database and reports the slowest tests, test files, and total time
spent in tests. It is designed to make profiling tests to improve their speed
easier.

[Github](https://github.com/etscrivner/nose-perfdump)
"""


setup(
    name='nose-perfdump',
    version=version,
    description='Dump per-test performance metrics to an SQLite database for querying.',
    long_description=long_desc,
    author='Eric Scrivner',
    keywords='nose,nose plugin,profiler,profiling,tests,unittest',
    install_requires=['nose'],
    author_email='eric.t.scrivner@gmail.com',
    url='https://github.com/etscrivner/nose-perfdump',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'nose.plugins.0.10': [
            'perfdump = perfdump:PerfDumpPlugin'
        ]
    }
)
