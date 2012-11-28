import inspect
import logging
import os
import sqlite3
import time

import nose
from nose.plugins import Plugin


sqlite_connection = sqlite3.connect('perfdump.db')
sqlite_connection.execute("CREATE TABLE IF NOT EXISTS times (file text, file_line int, module text, class text, func text, elapsed float)")
sqlite_connection.execute("DELETE FROM times")


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
    
    def get_file_line(self, test):
        """Returns the line number in the given file containing the given test.

        :param test: The test being run
        :type test: nose.case.Test
        
        """
        return inspect.getsourcelines(test.test.__class__)[1]

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
        q = "INSERT INTO times VALUES('{}', '{}', '{}', '{}', '{}', {})"
        self.db.execute(q.format(self.get_test_file(test),
                                 self.get_file_line(test),
                                 self.get_module_name(test),
                                 self.get_class_name(test),
                                 self.get_function_name(test),
                                 elapsed))

    def report(self, stream):
        """Displays the slowest tests"""
        self.db.commit()
    
    def finalize(self, result):
        """Perform final cleanup for this plugin."""
        self.db.close()

        
if __name__ == '__main__':
    nose.main(addplugins=[PerfDumpPlugin()])
