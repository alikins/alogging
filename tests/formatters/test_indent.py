import logging
import alogging

from alogging.formatters.indent import IndentFormatter
log = alogging.get_logger()

def test_indent_formatter_by_logger_name_depth():
    log_record = logging.makeLogRecord({
        'duration': 0.9,
        'created': 1621620910.5428703,
        'exc_info': None,
        'exc_text': None,
        'filename': 'module.py',
        'funcName': 'noisy_method',
        'levelname': 'DEBUG',
        'levelno': 10,
        'lineno': 42,
        'module': 'somemodule',
        'msecs': 542.870283126831,
        'msg': 'stuff %s',
        'name': 'first.second.third.forth.fifth',
        'pathname': '/first/second/third/module.py',
        'process': 1563624,
        'processName': 'MainProcess',
        'relativeCreated': 240.27323722839355,
        'stack_info': None,
        'args': "ThisParticularStuff",
        'thread': 140653102278464,
        'threadName': 'MainThread'}
    )

    indent_string = '|'
    indent_formatter = IndentFormatter(indent_string=indent_string)
    res = indent_formatter.format(log_record)
    print('%s|%s' % (res, log_record.name))
    depth = 4
    expected_indent = indent_string*depth
    expect_indent_len = len(expected_indent)
    assert res[0:expect_indent_len] == expected_indent

    log_record.name = "first.second.third"
    res = indent_formatter.format(log_record)
    print('%s|%s' % (res, log_record.name))
    # log.debug('|%s res: %s', log_record.name, res)

    log_record.name = "first"
    res = indent_formatter.format(log_record)
    print('%s|%s' % (res, log_record.name))
    # log.debug('|%s res: %s', log_record.name, res)

def test_indent_formatter_by_pathname_depth():
    log_record = logging.makeLogRecord({
        'duration': 0.9,
        'created': 1621620910.5428703,
        'exc_info': None,
        'exc_text': None,
        'filename': 'module.py',
        'funcName': 'noisy_method',
        'levelname': 'DEBUG',
        'levelno': 10,
        'lineno': 42,
        'module': 'somemodule',
        'msecs': 542.870283126831,
        'msg': 'stuff: %s',
        'name': 'first.second.third.forth.fifth',
        'pathname': '/first/second/third/module.py',
        'process': 1563624,
        'processName': 'MainProcess',
        'relativeCreated': 240.27323722839355,
        'stack_info': None,
        'args': "ThisParticularStuff",
        'thread': 140653102278464,
        'threadName': 'MainThread'}
    )

    indent_string = '/ '

    indent_formatter = IndentFormatter(indent_string=indent_string,
                                       indent_by='pathname_depth')

    res = indent_formatter.format(log_record)
    print('%s|%s' % (res, log_record.pathname))

    log_record.pathname = "/first/second/third/fourth/somemodule.py"
    res = indent_formatter.format(log_record)
    print('%s|%s' % (res, log_record.pathname))

    log_record.pathname = "/first/somemodule.py"
    res = indent_formatter.format(log_record)
    print('%s|%s' % (res, log_record.pathname))
