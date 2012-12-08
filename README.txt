nose-perfdump
=============

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

    ..
    
    10 slowest test times
    ----------
    
    2.00133s /test_something.py
             test_something.AddTest.test_slow_addition
    
    0.00072s /test_something.py
             test_something.AddTest.test_addition
    
    ----------
    
    2.00205s /test_something.py
    
    ----------
    
    Total time: 2.00205s
    
    
    10 slowest setup times
    ----------
    
    0.00000s /test_something.py
             test_something.AddTest.setUp
    
    0.00000s /test_something.py
             test_something.AddTest.setUp
    
    ----------
    
    0.00001s /test_something.py
    
    ----------
    
    Total time: 0.00001s
    
    ----------------------------------------------------------------------
    Ran 2 tests in 2.026s
    
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
