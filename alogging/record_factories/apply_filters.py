import logging

# TODO: seems like this should be scoped in a callable
#       so that 'original_factory' is the log_record_factory
#       at a more intentional explicity point instead of just
#       whenever this module gets imported

original_factory = logging.getLogRecordFactory()


def default_filters_factory(*args, **kwargs):
    record = original_factory(*args, **kwargs)
    return record


class ApplyFiltersRecordFactory:
    def __init__(self, *args, filters=None, base_factory=None, **kwargs):
        """Apply each of the log record filter instances in `filters` in order on every log record created

        Using logging.setLogRecordFactory(ApplyFiltersRecordFactory(filters=[...list of filter instances]))
        is equilivent to adding the set of filters to every logger instance"""
        self.filters = filters or []
        self.base_factory = base_factory or logging.getLogRecordFactory()

    def __call__(self, name, level, fn, lno, msg, args, exc_info,
                 func=None, sinfo=None, **kwargs):
        record = self.base_factory(name, level, fn, lno, msg, args, exc_info,
                                   func=func, sinfo=sinfo, **kwargs)

        # log record filters modify log record as a side effect (if they modify it).
        # For the use here, we also ignore the boolean returned by filter()
        for record_filter in self.filters:
            # Based on logging.Filterers.filter() but ignores returned value
            if hasattr(record_filter, 'filter'):
                record_filter.filter(record)
            else:
                record_filter(record)

        return record
