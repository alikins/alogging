import logging
import os
import pprint

import pytest

import alogging
import alogging.filters.exclude

log = alogging.get_logger()

@pytest.fixture
def log_record():
    record_factory = logging.getLogRecordFactory()
    log_record = record_factory('annoying',
                                logging.DEBUG,
                                '/dev/null/fake/module.py',
                                42,
                                "stuff_you_dont_to_hear: %s",
                                args=('whatever',),
                                exc_info=None,
                                func='noisy_method',
                                sinfo=None)
    return log_record


def test_no_excludes(log_record):
    exclude_filter = alogging.filters.exclude.ExcludeFilter()

    kept = exclude_filter.filter(log_record)
    assert kept is True
    log.debug('log_record: %s', log_record)
    # verify we didn't zero out the record
    assert log_record.name == 'annoying'


def test_exclude_annoying_logger(log_record):
    exclude_filter = \
        alogging.filters.exclude.ExcludeFilter(
            excludes=[('name', 'annoying')],
            operator='ALL')

    kept = exclude_filter.filter(log_record)
    assert kept is False
    log.debug('log_record: %s', log_record)

