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

import cmd
from pyparsing import Keyword, ParseException
import re
import perfdump.models

# Keywords
t_slowest = Keyword('slowest')
t_fastest = Keyword('fastest')

t_test = Keyword('test')
t_setup = Keyword('setup')

t_file = Keyword('file')
t_module = Keyword('module')
t_class = Keyword('class')
t_func = Keyword('function')

t_group_by = Keyword('groupby')

# SortOrder = T_SLOWEST | T_FASTEST
t_sort_order = (t_slowest ^ t_fastest)
# TimeSet = T_TEST | T_SETUP
t_time_set = (t_test ^ t_setup)
# Grouping = T_GROUP_BY
grouping = t_group_by + (t_file ^ t_module ^ t_class ^ t_func)

# Stmt = SortOrder TimeSet | SortOrder TimeSet Grouping
stmt = (t_sort_order + t_time_set) ^ (t_sort_order + t_time_set + grouping)

class Console(cmd.Cmd):
    """Console for querying perfdump results"""
    
    prompt = "perfdump > "

    def precmd(self, line):
        """Parse the command on the given line.
        
        :param line: The raw input line
        :type line: str
        
        """
        line = line.lower()
        
        if line == 'exit':
            return line
        
        try:
            parts = stmt.parseString(line)
            print line, "->", parts

            if len(parts) == 2:
                return "simple_report"
            else:
                return "grouped_report"
        except ParseException, err:
            pass
        
        return ""

    def do_simple_report(self, line):
        parts = stmt.parseString(line)

    def do_grouped_report(self, line):
        pass
            
    def do_exit(self, line):
        """End the console process."""
        return True
    

def main():
    """Entry-point for perfdump console."""
    Console().cmdloop()
    
    
if __name__ == "__main__":
    main()
