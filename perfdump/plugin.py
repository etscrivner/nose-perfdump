import os
import time

from nose.plugins import Plugin

from perfdump.connection import SqliteConnection
from perfdump.models import TestTime, MetaTest


class PerfDumpPlugin(Plugin):
    """Nose plugin that will collect and write to an SQLite database per-test
    elapsed times and print out the slowest 10 tests in your codebase."""
    
    name = 'perfdump'
    times = {}

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

    def beforeTest(self, test):
        """Records the base time before the test is run."""
        self.times[test.id()] = time.clock()

    def afterTest(self, test):
        """Records the complete test performance information after it is run"""
        elapsed = time.clock() - self.times[test.id()]
        del self.times[test.id()]
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
