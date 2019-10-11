import logging

import sqlparse
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import Terminal256Formatter


class DjangoDbSqlColorFormatter(logging.Formatter):
    '''pretty print django.db sql with color by pyments'''

    def __init__(self, fmt=None, datefmt=None, options=None):
        super(DjangoDbSqlColorFormatter, self).__init__(fmt=fmt, datefmt=datefmt)

        self.options = options or {'reindent': True,
                                   'keyword_case': 'upper'}

        self._lexer = SqlLexer()
        self._formatter = Terminal256Formatter()

    def format(self, record):
        pretty_sql = sqlparse.format(record.sql,
                                     **self.options)

        pretty_sql = highlight(pretty_sql, self._lexer, self._formatter)
        record.sql = pretty_sql
        # import pprint
        # return '\n__dict__=%s\n' % pprint.pformat(record.__dict__)
        return super(DjangoDbSqlColorFormatter, self).format(record)

    def __repr__(self):
        buf = '%s(fmt="%s", options=%s)' % (self.__class__.__name__, self._fmt, self.options)
        return buf
