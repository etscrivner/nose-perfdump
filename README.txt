nose-perfdump
=============

Nose plugin that provides per-test performance metrics. Useful mainly for
finding slow tests in need of optimization. Adds two additional flags to
nose.

    --with-perfdump - Enables perfdump output

    --perfdump-html=[path-to-file] - Dump the full perfdump output to HTML file

The output of perfdump in the console looks something like the following:

    Test times
    ----------
    
    0.00065s /test_something.py
             test_something.AddTest.test_something
    
    ----------
    
    0.00065s /test_something.py
    
    ----------
    
    Total time: 0.00065s
    
    
    Setup times
    ----------
    
    0.00000s /test_something.py
             test_something.AddTest.setUp
    
    ----------
    
    0.00000s /test_something.py
    
    ----------
    
    Total time: 0.00000s
