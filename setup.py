#!/usr/bin/env python

from setuptools import setup, find_packages


version = '1.7'


long_desc = """
nose-perfdump is a nose plugins to help profile and determine the slowest tests
in your test suite.

[Github](https://github.com/etscrivner/nose-perfdump)
"""


setup(
    name='nose-perfdump',
    version=version,
    description='Nose plugins to help determine the slowest tests in your test suite.',
    long_description=long_desc,
    author='Eric Scrivner',
    keywords='nose,nose plugin,profiler,profiling,tests,unittest',
    install_requires=['nose', 'pyparsing', 'prettytable'],
    author_email='eric.t.scrivner@gmail.com',
    url='https://github.com/etscrivner/nose-perfdump',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'nose.plugins.0.10': [
            'perfdump = perfdump:PerfDumpPlugin'
        ],
        'console_scripts': [
            'perfdump-cli = perfdump.console:main'
        ]
    }
)
