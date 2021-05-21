import logging
import os
import pprint

import alogging
import alogging.filters.exclude

log = alogging.get_logger()

def test_no_excludes():
    exclude_filter = alogging.filters.exclude.ExcludeFilter()

    record_factory = logging.getLogRecordFactory()
    log_record = record_factory('test',
                                logging.DEBUG,
                                '/dev/null/fake/module.py',
                                42,
                                "stuff_you_dont_to_hear: %s",
                                args=('whatever',),
                                exc_info=None,
                                func='noisy_method',
                                sinfo=None)

    kept = exclude_filter.filter(log_record)
    assert kept is True
    log.debug('log_record: %s', log_record)
    # verify we didn't zero out the record
    assert log_record.name == 'test'


