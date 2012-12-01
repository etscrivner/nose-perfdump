import cmd


class Console(cmd.Cmd):
    """Console for querying perfdump results"""
    
    def do_exit(self, line):
        """End the console process."""
        return True
    

def main():
    """Entry-point for perfdump console."""
    Console.cmdloop()