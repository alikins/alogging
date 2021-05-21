
import getpass
import os
import sys


class CurrentProcess(object):
    """Info about current process.

    logging.LogRecords include 'processName', but it is also fairly
    bogus (ie, 'MainProcess').

    So check sys.argv for a better name. Also get current user."""

    def __init__(self, args=None):
        self.args = args or sys.argv[:]
        self.cmd_name = os.path.basename(self.args[0])
        self.cmd_line = ' '.join(self.args)
        # is getpass useful in modules? windows?
        self.user = getpass.getuser()


# Don't need this for syslog
class ProcessContextLoggingFilter(object):
    """Filter that adds cmd_name, cmd_line, and user to log records

    cmd_name is the basename of the executable running ('myscript.py')
     as opposed to log record field 'processName' which is typically something
     like 'MainProcess'.

    cmd_line is the full cmdline. ie, sys.argv joined to a string,

    user is the user the process is running as."""

    def __init__(self, name=""):
        self.name = name
        self._current_process = CurrentProcess(args=sys.argv[:])

    def filter(self, record):
        record.cmd_name = self._current_process.cmd_name
        record.cmd_line = self._current_process.cmd_line
        record.user = self._current_process.user

        return True
