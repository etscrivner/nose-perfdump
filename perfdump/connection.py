import os
import sqlite3


class SqliteConnection(object):
    """Singleton class for obtaining an SQLite3 connection."""

    @classmethod
    def connect(cls, dbname):
        """Create a new connection to the SQLite3 database.

        :param dbname: The database name
        :type dbname: str
        
        """
        test_times_schema = """
        CREATE TABLE IF NOT EXISTS test_times (
          file text,
          module text,
          class text,
          func text,
          elapsed float
        )
        """
        
        setup_times_schema = """
        CREATE TABLE IF NOT EXISTS setup_times (
          file text,
          module text,
          class text,
          func text,
          elapsed float
        )
        """
        
        schemas = [test_times_schema,
                   setup_times_schema]
        
        db_file = '{}.db'.format(dbname)
        
        try:
            os.remove(db_file)
        except:
            pass
        
        cls.connection = sqlite3.connect(db_file)
        for s in schemas:
            cls.connection.execute(s)
                
    @classmethod
    def get(cls, dbname="perfdump"):
        """Returns the singleton connection to the SQLite3 database.

        :param dbname: The database name
        :type dbname: str
        
        """
        try:
            return cls.connection
        except:
            cls.connect(dbname)
            return cls.connection
