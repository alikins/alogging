import logging

import sqlparse


class DjangoDbSqlFormatter(logging.Formatter):
    '''pretty print django.db sql'''

    def __init__(self, fmt=None, datefmt=None, options=None):
        super(DjangoDbSqlFormatter, self).__init__(fmt=fmt, datefmt=datefmt)

        self.options = options or {'reindent': True,
                                   'keyword_case': 'upper'}

    def format(self, record):
        pretty_sql = sqlparse.format(record.sql,
                                     **self.options)

        record.sql = pretty_sql
        # import pprint
        # return '\n__dict__=%s\n' % pprint.pformat(record.__dict__)
        return super(DjangoDbSqlFormatter, self).format(record)

    def __repr__(self):
        buf = 'DjangoDbSqlFormatter(fmt="%s", options=%s)' % (self._fmt, self.options)
        return buf
