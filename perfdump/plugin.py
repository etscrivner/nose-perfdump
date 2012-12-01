# This file is part of nose-perftest.
#
# Copyright (c) 2012, Eric Scrivner and AUTHORS
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the nose-perfdump nor the names of its contributors may be
#   used to endorse or promote products derived from this software without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from functools import wraps
import inspect
import os
import time

from nose.plugins import Plugin

from perfdump.connection import SqliteConnection
from perfdump.models import MetaFunc, MetaTest, SetupTime, TestTime
from perfdump.html import HtmlReport


class PerfDumpPlugin(Plugin):
    """Nose plugin that will collect and write to an SQLite database per-test
    elapsed times and print out the slowest 10 tests in your codebase."""
    
    name = 'perfdump'
    
    test_times = {}
    setup_times = {}

    html_output_file = None

    @staticmethod
    def name_for_obj(i):
        if inspect.ismodule(i):
            return i.__name__
        else:
            return "%s.%s" % (i.__module__, i.__name__)

    def record_elapsed_decorator(self, f, ctx, key_name):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start_time = time.clock()
            try:
                return f(*args, **kwargs)
            finally:
                ctx[key_name] = time.clock() - start_time
                meta_func = MetaFunc.get(f)
                SetupTime.create(meta_func.file, 
                                 meta_func.module, 
                                 meta_func.cls,                                 
                                 key_name,
                                 ctx[key_name])

        return wrapped
    
    def __init__(self):
        super(PerfDumpPlugin, self).__init__()
        self.database_name = 'perfdump'
        try:
            os.remove('{}.db'.format(self.database_name))
        except:
            pass
        
    def options(self, parser, env=os.environ):
        """Handle parsing additional command-line options"""
        super(PerfDumpPlugin, self).options(parser, env=env)
        parser.add_option("", "--perfdump-html", dest="perfdump_html_file",
                          help="Set destination for HTML report output")

    def configure(self, options, conf):
        """Configure this plugin using the given options"""
        super(PerfDumpPlugin, self).configure(options, conf)
        if not self.enabled:
            return
        try:
            self.html_output_file = options.perfdump_html_file
        except:
            pass
        self.db = SqliteConnection.get(self.database_name)

    def startContext(self, context):
        ctx_name = self.name_for_obj(context)
        self.setup_times[ctx_name] = ctx = {'setUp': 0,
                                            'tearDown': 0}

        if hasattr(context, 'setUp'):
            for k in ['setUp']:#('setUp', 'tearDown'):
                old_f = getattr(context, k)
                new_f = self.record_elapsed_decorator(old_f, ctx, k)
                setattr(context, k, new_f)
    
    def beforeTest(self, test):
        """Records the base time before the test is run."""
        self.test_times[test.id()] = time.clock()

    def afterTest(self, test):
        """Records the complete test performance information after it is run"""
        elapsed = time.clock() - self.test_times[test.id()]
        del self.test_times[test.id()]
        meta_test = MetaTest.get(test)
        TestTime.create(meta_test.file,
                        meta_test.module,
                        meta_test.cls,
                        meta_test.func,
                        elapsed)

    def report(self, stream):
        """Displays the slowest tests"""
        self.db.commit()

        stream.writeln()
        stream.writeln("10 slowest test times")
        self.draw_divider(stream)
        
        self.display_slowest_tests(stream)
        
        stream.writeln()
        stream.writeln("10 slowest setup times")
        self.draw_divider(stream)
        self.display_slowest_setups(stream)

        if self.html_output_file:
            HtmlReport.write(self.html_output_file)

    def draw_divider(self, stream):
        """Draw a set of line dividers"""
        stream.writeln('-'*10)
        stream.writeln()
        
    def display_slowest_tests(self, stream):
        """Prints a report regarding the slowest individual tests."""
        # Display the slowest individual tests
        slowest_tests = TestTime.get_slowest_tests(10)
        for row in slowest_tests:
            stream.writeln('{:.05f}s {}'.format(row['elapsed'],
                                                row['file'])) 
            stream.writeln('{:9}{}.{}.{}'.format('',
                                                 row['module'],
                                                 row['class'],
                                                 row['func']))
            stream.writeln()

        stream.writeln('-'*10)
        stream.writeln()

        # Display the slowest test files
        slowest_files = TestTime.get_slowest_files(10)
        for row in slowest_files:
            stream.writeln('{:.05f}s {}'.format(row['sum_elapsed'],
                                                row['file']))
            stream.writeln()

        # Display the total time spent in tests
        stream.writeln('-'*10)
        stream.writeln()
        stream.writeln('Total time: {:.05f}s'.format(TestTime.get_total_time()))
        
        stream.writeln()
        
    def display_slowest_setups(self, stream):
        """Prints a report regarding the slowest setUp/tearDown times."""
        slowest_tests = SetupTime.get_slowest_tests(10)
        for row in slowest_tests:
            stream.writeln('{:.05f}s {}'.format(row['elapsed'],
                                                row['file'])) 
            stream.writeln('{:9}{}.{}.{}'.format('',
                                                 row['module'],
                                                 row['class'],
                                                 row['func']))
            stream.writeln()

        stream.writeln('-'*10)
        stream.writeln()

        # Display the slowest test files
        slowest_files = SetupTime.get_slowest_files(10)
        for row in slowest_files:
            stream.writeln('{:.05f}s {}'.format(row['sum_elapsed'],
                                                row['file']))
            stream.writeln()

        # Display the total time spent in tests
        stream.writeln('-'*10)
        stream.writeln()
        stream.writeln('Total time: {:.05f}s'.format(SetupTime.get_total_time()))
        
        stream.writeln()
    
    def finalize(self, result):
        """Perform final cleanup for this plugin."""
        self.db.close()
