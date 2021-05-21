import logging


class DjangoDbSqlSlowQueriesFilter(logging.Filter):
    '''Filter to log only "slow" sql queries

    Default is to only show queries that take more than 40ms

    The min_duration init arg is in seconds. Default is 0.04s (40ms)

    Add this filter to handlers that get log records from 'django.db' loggers.

    See django_sql_slow_queries_example.yaml for yaml setup.
    '''

    def __init__(self, name="", min_duration=0.04):
        super(DjangoDbSqlSlowQueriesFilter, self).__init__(name=name)
        # Can raise a ValueError
        self.min_duration = float(min_duration) or 0.04

    def filter(self, record):
        duration = getattr(record, 'duration', None)
        if not duration:
            return 1

        # NOTE: the 'duration' record is a string, not a float.
        try:
            f_duration = float(duration)
        except ValueError:
            # bogus duration field value, just drop this log line
            return 0

        if f_duration > self.min_duration:
            return 1

        # ignore queries shorter than min_duration
        return 0

    def __repr__(self):
        return f"{__name__}.{self.__class__.__name__}(min_duration={self.min_duration})"
