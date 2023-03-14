import logging
import os

class IndentFormatter(logging.Formatter):
    '''Indent the output based on logger depth.'''
    def __init__(self, fmt=None, datefmt=None, style='%',
                 indent_by=None, indent_string=None):
        super(IndentFormatter, self).__init__(fmt=fmt,
                                              datefmt=datefmt,
                                              style=style)
        self.indent_by = indent_by or 'logger_depth'
        self.indent_string = indent_string or ' '

    def _prepend_indent_attr(self, style, fmt):
        '''Prepend a 'indent' attr to the log fmt if needed'''

        if '%(indent)s' in fmt or '{indent}' in fmt:
            return fmt
        if isinstance(style, logging.PercentStyle):
            return '%(indent)s' + fmt
        if isinstance(style, logging.StrFormatStyle):
            return '{indent}' + fmt
        return fmt

    def format(self, record):
        self._style._fmt = self._prepend_indent_attr(style=self._style, fmt=self._fmt)
        depth = self.get_depth(record)
        indent_blob = self.indent_string*depth
        record.indent = indent_blob
        return super().format(record)

    def by_logger_depth(self, record):
        dot_count = record.name.count('.')
        return dot_count

    def by_pathname_depth(self, record):
        dir_count = record.pathname.count(os.sep)
        return dir_count

    def get_depth(self, record):
        if self.indent_by == 'logger_depth':
            return self.by_logger_depth(record)
        if self.indent_by == 'pathname_depth':
            return self.by_pathname_depth(record)
        return 0
