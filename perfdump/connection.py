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
# * Neither the name of the cqlengine nor the names of its contributors may be
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
