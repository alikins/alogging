import logging
import pprint

import alogging
import alogging.filters.process_context

log = alogging.get_logger()


def test_current_process():
    current_process = alogging.filters.process_context.CurrentProcess()
    log.debug('current_process: %s', current_process)
    log.debug(pprint.pformat(current_process.__dict__))


def test_process_context_logging_filter():
    current_process = alogging.filters.process_context.CurrentProcess()
    cmd_name = "/usr/fake/bin/fake.py"
    current_process.cmd_name = cmd_name
    cmd_line = current_process.cmd_name + " --turbo -abcdfgh /dev/null/fakefile"
    current_process.cmd_line = cmd_line
    current_process.user = "testuser"

    log_filter = alogging.filters.process_context.ProcessContextLoggingFilter('filter_name')
    log_filter._current_process = current_process

    record_factory = logging.getLogRecordFactory()
    log_record = record_factory('test', logging.DEBUG, '/usr/fake/lib/fake.py', 42, "some msg: %s",
                                args=('fake_message',), exc_info=None, func='fake_method', sinfo=None)

    kept = log_filter.filter(log_record)
    assert kept is True
    log.debug('log_record: %s', log_record)

    assert log_record.cmd_name == cmd_name
    assert log_record.user == "testuser"
    assert log_record.cmd_line == cmd_line
