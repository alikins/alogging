import logging

import alogging
from alogging.record_factories import apply_filters

log = alogging.get_logger()


class AddBlippynessFilter:
    def __init__(self, blippyness=None):
        self.blippyness = blippyness or 'very blippy'

    def filter(self, record):
        record.blippyness = self.blippyness
        return True


def add_mood_filter_method(record):
    record.mood = "2020 is 2020'ing again"
    return True


def test_apply_filters_record_factory():
    pathname = '/usr/fake/lib/fake.py',

    filters = [AddBlippynessFilter(blippyness="moderate blip likely"),
               add_mood_filter_method]

    factory = apply_filters.ApplyFiltersRecordFactory(filters=filters,
                                                      base_factory=logging.getLogRecordFactory())
    log_record = factory(name='test',
                         level=logging.DEBUG,
                         fn=pathname,
                         lno=42,
                         msg="some msg: %s",
                         args=('fake_message',),
                         exc_info=None,
                         func='fake_method',
                         sinfo=None)

    log.debug('log_record: %s', log_record)

    assert log_record.levelno == logging.DEBUG
    assert log_record.levelname == "DEBUG"
    assert log_record.pathname == pathname
    assert log_record.blippyness == "moderate blip likely"
    assert log_record.mood == "2020 is 2020'ing again"


def test_apply_filters_record_factory_as_default():
    original_factory = logging.getLogRecordFactory()

    # TODO: setup a faux test handler, or I guess, use mock to check the calls
    try:
        filters = [AddBlippynessFilter(blippyness="moderate blip likely"),
                   add_mood_filter_method]
        factory = apply_filters.ApplyFiltersRecordFactory(filters=filters,
                                                          base_factory=original_factory)
        logging.setLogRecordFactory(factory)

        log.debug('This is a test msg: %s', "foo", extra={'tsx_id': 42})
    except Exception as exc:
        log.exception(exc)
    finally:
        logging.setLogRecordFactory(original_factory)
