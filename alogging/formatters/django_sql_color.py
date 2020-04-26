import logging

import sqlparse
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name


class DjangoDbSqlColorFormatter(logging.Formatter):
    '''Pretty print django.db sql with color by pyments'''

    def __init__(self, fmt=None, datefmt=None, options=None, style='%',
                 pygments_lexer='postgres-console',
                 pygments_formatter="terminal256",
                 pygments_style="default"):
        super(DjangoDbSqlColorFormatter, self).__init__(fmt=fmt,
                                                        datefmt=datefmt,
                                                        style=style)

        self.options = options or {'reindent': True,
                                   'keyword_case': 'upper'}

        # postgres-console, postgres, rql, sql, sqlite3, mysql, plpgsql, tsql
        self._lexer = get_lexer_by_name(pygments_lexer)

        pygments_style = get_style_by_name(pygments_style)

        # terminal256, terminal, terminal16m, text
        self._formatter = get_formatter_by_name(pygments_formatter, style=pygments_style)

    def format(self, record):
        pretty_sql = sqlparse.format(record.sql,
                                     **self.options)

        pretty_sql = highlight(pretty_sql, self._lexer, self._formatter)
        record.sql = pretty_sql
        return super(DjangoDbSqlColorFormatter, self).format(record)

    def __repr__(self):
        buf = '%s(fmt="%s", options=%s)' % (self.__class__.__name__, self._fmt, self.options)
        return buf
