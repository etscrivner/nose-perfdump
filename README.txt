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

    10 slowest test times
    ----------
    
    0.00065s /test_something.py
             test_something.AddTest.test_something
    
    ----------
    
    0.00065s /test_something.py
    
    ----------
    
    Total time: 0.00065s
    
    
    10 slowest setup times
    ----------
    
    0.00000s /test_something.py
             test_something.AddTest.setUp
    
    ----------
    
    0.00000s /test_something.py
    
    ----------
    
    Total time: 0.00000s
