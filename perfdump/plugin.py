from functools import wraps
import inspect
import os
import time

from nose.plugins import Plugin

from perfdump.connection import SqliteConnection
from perfdump.models import MetaFunc, MetaTest, SetupTime, TestTime


class PerfDumpPlugin(Plugin):
    """Nose plugin that will collect and write to an SQLite database per-test
    elapsed times and print out the slowest 10 tests in your codebase."""
    
    name = 'perfdump'
    test_times = {}
    setup_times = {}

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
        
    def options(self, parser, env=os.environ):
        """Handle parsing additional command-line options"""
        super(PerfDumpPlugin, self).options(parser, env=env)

    def configure(self, options, conf):
        """Configure this plugin using the given options"""
        super(PerfDumpPlugin, self).configure(options, conf)
        if not self.enabled:
            return
        self.db = SqliteConnection.get(self.database_name)

    def startContext(self, context):
        ctx_name = self.name_for_obj(context)
        self.setup_times[ctx_name] = ctx = {'setUp': 0,
                                            'tearDown': 0}

        if hasattr(context, 'setUp'):
            for k in ('setUp', 'tearDown'):
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
        self.display_slowest_tests(stream)

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
    
    def finalize(self, result):
        """Perform final cleanup for this plugin."""
        self.db.close()
