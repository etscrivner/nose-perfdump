import logging
import os
import sqlite3
import time

import nose
from nose.plugins import Plugin


sqlite_connection = sqlite3.connect('perfdump.db')
sqlite_connection.execute("CREATE TABLE IF NOT EXISTS times (name text, elapsed float)")
sqlite_connection.execute("DELETE FROM times")


def get_connection():
    return sqlite_connection


class PerfDump(Plugin):
    """
    Nose plugin that will collect and write to an SQLite database per-test
    elapsed times and print out the slowest 10 tests in your codebase.
    """
    name = 'perfdump'
    times = {}
        
    def options(self, parser, env=os.environ):
        super(PerfDumpPlugin, self).options(parser, env=env)

    def configure(self, options, conf):
        super(PerfDumpPlugin, self).configure(options, conf)
        if not self.enabled:
            return
        self.db = get_connection()

    def beforeTest(self, test):
        self.times[test.id()] = time.clock()

    def afterTest(self, test):
        elapsed = time.clock() - self.times[test.id()]
        import ipdb; ipdb.set_trace()
        del self.times[test.id()]
        self.db.execute("INSERT INTO times VALUES('{}', {})".format(test.id(), elapsed))

    def report(self, stream):
        self.db.commit()
    
    def finalize(self, result):
        self.db.close()

        
if __name__ == '__main__':
    nose.main(addplugins=[PerfDumpPlugin()])
