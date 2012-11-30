import inspect
import os
import sqlite3

from perfdump.connection import SqliteConnection


class MetaFunc(object):
    """Represents meta-information regarding a given function."""
    
    @classmethod
    def get(cls, function):
        """Returns a new meta-function initialized with the given test.
        
        :param func: The function
        :type test: instancemethod
        
        """
        return MetaFunc(function)
    
    @property
    def file(self):
        """Return the name of the file containing the function."""
        return self.full_test_file.replace(os.getcwd(), '').replace('.pyc', '.py')
    
    @property
    def module(self):
        """Return the name of the module"""
        return inspect.getmodulename(self.full_test_file)
    
    @property
    def cls(self):
        """Return the class name"""
        return inspect.getmro(self.function.im_class)[0].__name__
    
    def __init__(self, function):
        """Initialize the class with the given instancemethod information.
        
        :param function: The function
        :type function: instancemethod
        
        """
        self.full_test_file = inspect.getfile(function.im_class)
        self.function = function
                
        
class MetaTest(object):
    """Represents meta-information regarding a given test."""
    
    @classmethod
    def get(cls, test):
        """Returns a new meta-test initialized with the given test.
        
        :param test: The test
        :type test: nose.case.Test
        
        """
        return MetaTest(test)
    
    @property
    def file(self):
        """Return the name of the file containing the test."""
        return self.full_test_file.replace(os.getcwd(), '').replace('.pyc', '.py')
    
    @property
    def module(self):
        """Return the name of the module containing the test."""
        return inspect.getmodulename(self.full_test_file)
    
    @property
    def cls(self):
        """Return the name of the test class."""
        return inspect.getmro(self.test.test.__class__)[0].__name__
    
    @property
    def func(self):
        """Return the name of the test function."""
        return self.test.id().split('.')[-1]
    
    def __init__(self, test):
        """Initialize this class with test information
        
        :param test: The test
        :type test: nose.case.Test
        
        """
        self.full_test_file = inspect.getfile(test.test.__class__)
        self.test = test
    
    
class BaseTimeModel(object):
    """Base class for a time sample."""
    
    @classmethod
    def create(cls, file, module, cls_name, func, elapsed):
        """Inserts a new time sample into the database with the given information.
        
        :param file: The file the sample is from
        :type file: str
        :param module: The module the sample is from
        :type module: str
        :param cls_name: The name of the class the sample is from
        :type cls_name: str
        :param func: The name of the function the sample is from
        :type func: str
        :param elapsed: The elapsed time in seconds
        :type elapsed: float
        
        """
        q = "INSERT INTO {} VALUES('{}', '{}', '{}', '{}', {})"
        SqliteConnection.get().execute(q.format(cls.meta['table'],
                                                file,
                                                module,
                                                cls_name,
                                                func,
                                                elapsed))

    @classmethod
    def is_valid_row(cls, row):
        """Indicates whether or not the given row contains valid data."""
        for k in row.keys():
            if row[k] is None:
                return False
        return True
        
    @classmethod
    def get_cursor(cls):
        """Return a message list cursor that returns sqlite3.Row objects"""
        db = SqliteConnection.get()
        db.row_factory = sqlite3.Row
        return db.cursor()
    
    @classmethod
    def get_slowest_tests(cls, num=10):
        """Returns the slow num tests.
        
        :param num: The maximum number of results to be returned.
        :type num: int
        
        """
        cur = cls.get_cursor()
        q = "SELECT * FROM {} ORDER BY elapsed DESC LIMIT {}"
        cur.execute(q.format(cls.meta['table'], num))
        return cur.fetchall()
    
    @classmethod
    def get_slowest_files(cls, num=10):
        """Returns the slowest num files.
        
        :param num: The maximum number of results to be returned
        :type num: int
        
        """
        cur = cls.get_cursor()
        q = "SELECT file, SUM(elapsed) as sum_elapsed FROM {} ORDER BY sum_elapsed DESC LIMIT {}"
        cur.execute(q.format(cls.meta['table'], num))
        result = cur.fetchall()
        # Don't return the weird invalid row if no tests were run
        if not all([cls.is_valid_row(x) for x in result]):
            return []
        return result
    
    @classmethod
    def get_total_time(cls):
        """Returns the total time taken across all results.
        
        :rtype: float
        
        """
        cur = cls.get_cursor()
        q = "SELECT SUM(elapsed) FROM {}"
        cur.execute(q.format(cls.meta['table']))
        result = cur.fetchone()['SUM(elapsed)']
        return result if result else 0.0
    
    
class TestTime(BaseTimeModel):
    """Represents a time metric for a single test."""
    
    meta = {
        'table': 'test_times'
    }
    

class SetupTime(BaseTimeModel):
    """Represents a time metric for a single test setup."""
    
    meta = {
        'table': 'setup_times'
    }
    
