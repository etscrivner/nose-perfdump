nose-perfdump
=============

[![PyPI version](https://img.shields.io/pypi/v/nose-perfdump.svg)](http://badge.fury.io/py/nose-perfdump)

Nose plugin that collects per-test performance metrics into an SQLite3 database and reports the slowest tests, test files, and total time
spent in tests. It is designed to make profiling tests to improve their speed
easier.

# Install

This plugin is hosted on PyPI and can be installed with the following command:

    pip install nose-perfdump

# Overview

Nose plugin that provides per-test performance metrics. Useful mainly for
finding slow tests in need of optimization. Adds two additional flags to
nose.

    --with-perfdump - Enables perfdump output

    --perfdump-html=[path-to-file] - Dump the full perfdump report to an HTML file

The output of perfdump in the console looks something like the following:
    
    =====================
    | 10 SLOWEST SETUPS |
    =====================
    
    Per setup breakdown
    +----------+--------------------------+-----------------------------------+
    | Elapsed  | File                     | Method                            |
    +----------+--------------------------+-----------------------------------+
    | 0.00001s | /tests/test_something.py | test_something.AdditionTest.setUp |
    | 0.00000s | /tests/test_something.py | test_something.AdditionTest.setUp |
    +----------+--------------------------+-----------------------------------+
    
    Per file breakdown
    +----------+--------------------------+
    | Elapsed  | File                     |
    +----------+--------------------------+
    | 0.00001s | /tests/test_something.py |
    +----------+--------------------------+
    
    Total setup time: 0.00001s

    ====================
    | 10 SLOWEST TESTS |
    ====================

    Per test breakdown
    +----------+--------------------------+------------------------------------------------+
    | Elapsed  | File                     | Method                                         |
    +----------+--------------------------+------------------------------------------------+
    | 1.07604s | /tests/test_something.py | test_something.AdditionTest.test_slow_addition |
    | 0.00106s | /tests/test_something.py | test_something.AdditionTest.test_fast_addition |
    +----------+--------------------------+------------------------------------------------+
    
    Per file breakdown
    +----------+--------------------------+
    | Elapsed  | File                     |
    +----------+--------------------------+
    | 1.07710s | /tests/test_something.py |
    +----------+--------------------------+
    
    Total test time: 1.07710s
    
    ----------------------------------------------------------------------
    Ran 2 tests in 1.082s

    OK

# CLI Tool

There is also a command-line interface (CLI) tool provided with nose-perfdump
called perfdump-cli that allows for easier querying of the sqlite database.
    
    perfdump > help
    
    Perfdump CLI provides a handful of simple ways to query your
    performance data.
    
    The simplest queries are of the form:
    
	    [slowest|fastest] [tests|setups]
    
    For example:
    
	    perfdump > slowest tests
    
    Prints the slowest 10 tests
    
    Additional grouping of results can be request.
    
	    perfdump > slowest tests groupby file
    
    Grouping options include:
    
	    file | module | class | function
