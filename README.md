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
+----------+--------------------------------------+-------------------------------------------------+
| Elapsed  | File                                 | Method                                          |
+----------+--------------------------------------+-------------------------------------------------+
| 0.00122s | /tests/assignment/test_assignment.py | test_assignment.TestReject.setUp                |
| 0.00121s | /tests/assignment/test_assignment.py | test_assignment.TestBaseAssignment.setUp        |
| 0.00121s | /tests/assignment/test_assignment.py | test_assignment.TestGetByHitId.setUp            |
| 0.00116s | /tests/assignment/test_assignment.py | test_assignment.TestApprove.setUp               |
| 0.00093s | /tests/assignment/test_assignment.py | test_assignment.BaseAssignmentTestCase.setUp    |
| 0.00062s | /tests/assignment/test_assignment.py | test_assignment.TestGetAnswerToQuestion.setUp   |
| 0.00055s | /tests/assignment/test_hit.py        | test_hit.TestDispose.setUp                      |
| 0.00029s | /tests/test_connection.py            | test_connection.TestMakeConnection.setUp        |
| 0.00024s | /tests/assignment/test_hit.py        | test_hit.TestCreateFromBotoHit.setUp            |
| 0.00024s | /tests/test_connection.py            | test_connection.TestMakeSandboxConnection.setUp |
+----------+--------------------------------------+-------------------------------------------------+

Per file breakdown
+----------+---------------------------------------+
| Elapsed  | File                                  |
+----------+---------------------------------------+
| 0.03545s | /tests/assignment/test_assignment.py  |
| 0.00279s | /tests/assignment/test_hit.py         |
| 0.00183s | /tests/test_connection.py             |
| 0.00093s | /tests/assignment/test_task_upload.py |
| 0.00035s | /tests/test_utils.py                  |
| 0.00023s | /tests/assignment/test_task.py        |
| 0.00011s | /tests/assignment/test_answer.py      |
+----------+---------------------------------------+

Total setup time: 0.04170s

====================
| 10 SLOWEST TESTS |
====================

Per test breakdown
+----------+--------------------------------------+-----------------------------------------------------------------------------------------+
| Elapsed  | File                                 | Method                                                                                  |
+----------+--------------------------------------+-----------------------------------------------------------------------------------------+
| 0.00383s | /tests/assignment/test_hit.py        | test_hit.TestTransformRawHits.test_should_return_appropriately_transformed_hits         |
| 0.00247s | /tests/assignment/test_assignment.py | test_assignment.TestBaseAssignment.test_should_have_correct_hit_id                      |
| 0.00232s | /tests/assignment/test_assignment.py | test_assignment.TestReject.test_should_pass_correct_arguments_to_connection             |
| 0.00228s | /tests/assignment/test_hit.py        | test_hit.TestGetReviewableByBatchId.test_should_only_return_hit_ids_that_are_in_batch   |
| 0.00227s | /tests/assignment/test_assignment.py | test_assignment.TestGetByHitId.test_should_wrap_assignment_class_around_each_result     |
| 0.00224s | /tests/assignment/test_assignment.py | test_assignment.TestGetByHitId.test_should_correctly_initialize_age                     |
| 0.00196s | /tests/assignment/test_assignment.py | test_assignment.TestBaseAssignment.test_should_correctly_initialize_age                 |
| 0.00193s | /tests/assignment/test_assignment.py | test_assignment.TestApprove.test_should_raise_error_if_no_boto_connection_given         |
| 0.00181s | /tests/assignment/test_assignment.py | test_assignment.TestGetByHitId.test_should_pass_correct_information_to_retrieval_method |
| 0.00174s | /tests/assignment/test_assignment.py | test_assignment.TestApprove.test_should_pass_correct_information_to_boto_connection     |
+----------+--------------------------------------+-----------------------------------------------------------------------------------------+

Per file breakdown
+----------+---------------------------------------+
| Elapsed  | File                                  |
+----------+---------------------------------------+
| 0.03068s | /tests/assignment/test_assignment.py  |
| 0.01476s | /tests/assignment/test_hit.py         |
| 0.00533s | /tests/assignment/test_task_upload.py |
| 0.00496s | /tests/assignment/test_task.py        |
| 0.00483s | /tests/test_connection.py             |
| 0.00324s | /tests/assignment/test_answer.py      |
| 0.00086s | /tests/test_utils.py                  |
+----------+---------------------------------------+

Total test time: 0.06465s
    
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
