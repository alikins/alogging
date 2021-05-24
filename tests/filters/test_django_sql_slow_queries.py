import logging
import pprint

import pytest

import alogging
from alogging.filters.django_sql_slow_queries import DjangoDbSqlSlowQueriesFilter

log = alogging.get_logger()


@pytest.fixture
def log_record():
    _log_record = logging.makeLogRecord({
        'duration': 0.9,
        'created': 1621620910.5428703,
        'exc_info': None,
        'exc_text': None,
        'filename': 'module.py',
        'funcName': 'noisy_method',
        'levelname': 'DEBUG',
        'levelno': 10,
        'lineno': 42,
        'module': 'module',
        'msecs': 542.870283126831,
        'msg': 'stuff: %s',
        'name': 'django.db',
        'pathname': '/dev/null/fake/module.py',
        'process': 1563624,
        'processName': 'MainProcess',
        'relativeCreated': 240.27323722839355,
        'stack_info': None,
        'thread': 140653102278464,
        'threadName': 'MainThread'}
    )

    return _log_record


def test_duration_larger_than_limit(log_record):
    # default duration is 0.04 secs
    slow_query_filter = DjangoDbSqlSlowQueriesFilter()

    kept = slow_query_filter.filter(log_record)

    # since this record was slow, we let it though
    log.debug('log_record: %s', pprint.pformat(log_record.__dict__))
    assert bool(kept) is True


def test_duration_smaller_than_limit(log_record):
    # Set duration lower bound at 2 seconds
    slow_query_filter = DjangoDbSqlSlowQueriesFilter(min_duration=2.0)

    kept = slow_query_filter.filter(log_record)

    # since this record was slow, we let it though
    log.debug('log_record: %s', pprint.pformat(log_record.__dict__))
    assert bool(kept) is False
