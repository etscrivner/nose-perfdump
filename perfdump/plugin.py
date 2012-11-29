import inspect
import logging
import os
import sqlite3
import time

import nose
from nose.plugins import Plugin


try:
    os.remove('perfdump.db')
except:
    pass

sqlite_connection = sqlite3.connect('perfdump.db')
sqlite_connection.execute("CREATE TABLE IF NOT EXISTS times (file text, module text, class text, func text, elapsed float)")


def get_connection():
    return sqlite_connection


class PerfDumpPlugin(Plugin):
    """
    Nose plugin that will collect and write to an SQLite database per-test
    elapsed times and print out the slowest 10 tests in your codebase.
    """
    name = 'perfdump'
    times = {}

    def get_test_file(self, test):
        """Returns the partial path from the current working directory for the
        file containing the given test.

        :param test: The test being run
        :type test: nose.case.Test
        :rtype: str

        """
        full_test_file = inspect.getfile(test.test.__class__)
        return full_test_file.replace(os.getcwd(), '')

    def get_module_name(self, test):
        """Returns the name of the module containing the given test.

        :param test: The test being run
        :type test: nose.case.Test

        """
        full_test_file = inspect.getfile(test.test.__class__)
        return inspect.getmodulename(full_test_file)

    def get_class_name(self, test):
        """Returns the name of the test class containing this test.

        :param test: The test being run
        :type test: nose.case.Test

        """
        return inspect.getmro(test.test.__class__)[0].__name__

    def get_function_name(self, test):
        """Returns the name of the test function.

        :param test: Test
        :type test: nose.case.Test

        """
        return test.id().split('.')[-1]
        
    def options(self, parser, env=os.environ):
        """Handle parsing additional command-line options"""
        super(PerfDumpPlugin, self).options(parser, env=env)

    def configure(self, options, conf):
        """Configure this plugin using the given options"""
        super(PerfDumpPlugin, self).configure(options, conf)
        if not self.enabled:
            return
        self.db = get_connection()

    def beforeTest(self, test):
        """Records the base time before the test is run."""
        self.times[test.id()] = time.clock()

    def afterTest(self, test):
        """Records the complete test performance information after it is run"""
        elapsed = time.clock() - self.times[test.id()]
        del self.times[test.id()]
        q = "INSERT INTO times VALUES('{}', '{}', '{}', '{}', {})"
        self.db.execute(q.format(self.get_test_file(test),
                                 self.get_module_name(test),
                                 self.get_class_name(test),
                                 self.get_function_name(test),
                                 elapsed))

    def report(self, stream):
        """Displays the slowest tests"""
        self.db.commit()

        stream.writeln()

        self.db.row_factory = sqlite3.Row
        cur = self.db.cursor()
        cur.execute("SELECT * FROM times ORDER BY elapsed DESC LIMIT 10")
        row = cur.fetchone()
        while row:
            stream.writeln('{:.04f}s {}'.format(row['elapsed'],
                                                row['file'])) 
            stream.writeln('{:8}{}.{}.{}'.format('',
                                                 row['module'],
                                                 row['class'],
                                                 row['func']))
            stream.writeln()
            row = cur.fetchone()

        stream.writeln('-'*10)
        stream.writeln()
        
        cur.execute('SELECT file, SUM(elapsed) FROM times GROUP BY file ORDER BY SUM(elapsed) DESC LIMIT 10')
        row = cur.fetchone()
        while row:
            stream.writeln('{:.04f}s {}'.format(row['SUM(elapsed)'],
                                                row['file']))
            stream.writeln()
            row = cur.fetchone()

        cur.execute('SELECT SUM(elapsed) FROM times')
        row = cur.fetchone()
        stream.writeln('-'*10)
        stream.writeln()
        stream.writeln('Total time: {}s'.format(row['SUM(elapsed)']))
        
        stream.writeln()
    
    def finalize(self, result):
        """Perform final cleanup for this plugin."""
        self.db.close()
