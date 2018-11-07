
import functools
import inspect
import logging
import os
import sys

HAS_COLOR_DEBUG = False
try:
    # https://github.com/alikins/color_debug
    import color_debug
    HAS_COLOR_DEBUG = True
except ImportError as e:
    print(e)

# set to True if on py3 and you want stack_info log record populated
# WARNING: STACK_INFO=True is not compatible with py2 and will break
STACK_INFO = False

DEFAULT_FMT_STRING = """%(asctime)s %(relativeCreated)d %(levelname)-0.1s %(name)s %(process)d %(funcName)s:%(lineno)d - %(message)s"""

# for use with datefmt="%H:%M:%S" if you still want the ',123' msec info
NO_DATE_FMT_STRING = """%(asctime)s,%(msecs)03d %(levelname)-0.1s %(name)s %(processName)s:%(process)d %(funcName)s:%(lineno)d - %(message)s"""
STACK_INFO_FMT_STRING = """ %(stack_info)s"""

COLON_FMT_STRING = '%(asctime)s processName:%(processName)s process:%(process)d threadName ' + \
    '%(threadName)-2s level: %(levelname)s module: %(module)s name: %(name)s ' + \
    'funcName: %(funcName)s lineno: %(lineno)d %(message)s'

EVERYTHING_FMT_STRING = '%(asctime)s %(levelname)-0.1s %(levelno)-0.1d %(processName)-0.1s ' + \
    '%(process)d %(threadName)s %(thread)d %(name)s %(module)s %(filename)s %(funcName)s %(lineno)d - %(message)s'

DEFAULT_FILE_FMT_STRING = DEFAULT_FMT_STRING
DEFAULT_STREAM_FMT_STRING = NO_DATE_FMT_STRING
DEFAULT_FILE_DATEFMT_STRING = DEFAULT_STREAM_DATEFMT_STRING = DEFAULT_DATEFMT_STRING = None

# TODO: add a stack depth indicator filter?
#       filter would expect 'extra' to have a 'stack_depth' int attribute
#       The filter would replace value of 'stack_depth' with a string that
#       is basically '.' * stack_depth.
#       That adds a visual indicator to log lines about the stack depth

# TODO: method for setting a logger level by env var
# loglevel.ansible.inventory.manager.Manager=DEBUG ansible-playbook -v


def env_log_level(var_name):

    # be liberal in log env var name cap
    for env_var_candidates in (var_name, var_name.upper(), var_name.lower()):
        # print(env_var_candidates)
        env_var_value = os.environ.get(var_name, None)
        if env_var_value is not None:
            continue

    # print('%s=%s' % (var_name, env_var_value))

    if not env_var_value:
        return None

    env_var_value = env_var_value.strip()

    log_level = getattr(logging, env_var_value, env_var_value)

    try:
        log_level = int(log_level)
    except ValueError:
        raise Exception('the log level %s is not known' % env_var_value)

    return log_level


def get_logger_name(depth=None):
    depth = depth or 1
    called_from = inspect.stack()[depth]
    called_from_module = inspect.getmodule(called_from[0])
    return called_from_module.__name__


def get_class_logger_name(obj, depth=None):
    '''Use to get a logger name equiv to module.Class'''
    depth = depth or 1
    # pprint.pprint(inspect.stack())
    called_from = inspect.stack()[depth]
    called_from_module = inspect.getmodule(called_from[0])
    called_from_module_name = called_from_module.__name__
    # if obj has a name, use it, else check it's class name
    # This supports being pass a cls like in a meta class __new__ or a classmethor
    #  of being passed self as used in a class init
    obj_name = getattr(obj, '__name__', obj.__class__.__name__)
    return '%s.%s' % (called_from_module_name, obj_name)


# dont really need this, a log record has funcName
def get_method_logger_name(depth=None):
    depth = depth or 1
    called_from = inspect.stack()[depth]
    called_from_method = called_from[3]
    # called_from_module = inspect.getmodule(called_from[0])
    return called_from_method


def get_logger(name=None, depth=2):
    '''Use to get a logger with name of callers __name__

    Can be used in place of:

        import logging
        log = logging.getLogger(__name__)

    That can be replaced with

        from akl import alogging
        log = alogging.get_logger()
    '''
    name = name or get_logger_name(depth=depth)
    return logging.getLogger(name)


def get_class_logger(obj, depth=2):
    '''Use to get a logger with name equiv to module.Class

    in a regular class __init__, use like:

        self.log = alogging.get_class_logger(self)


    In a metaclass __new__, use like:

        log = alogging.get_class_logger(cls)
    '''

    return logging.getLogger(get_class_logger_name(obj, depth=depth))


def get_method_logger(depth=2):
    return logging.getLogger(get_method_logger_name(depth=depth))


def a(*args):

    log_name = get_logger_name(depth=2)
    log = logging.getLogger(log_name)
    if STACK_INFO:
        log._log(logging.DEBUG, 'd args=%s', repr(args), stack_info=True)
    else:
        log._log(logging.DEBUG, 'd args=%s', repr(args))

    # walk up the stack to find the first named logger?
    return args and args[0]


def t(func):
    log_name = get_method_logger_name(depth=2)
    log = logging.getLogger(log_name)
    log.debug('foo1, log_name=%s', log_name)

    log_name1 = get_logger_name(depth=2)
    # log1 = logging.getLogger(log_name1)
    # log1.debug('bar2, log_name_1=%s', log_name1)

    # log_name = get_class_logger_name(func, depth=2)
    # log_name = get_class_logger_name(func, depth=2)
    # log = logging.getLogger(log_name)
    # log.debug('cccccccc, log_name=%s', log_name)

    log2_name = '%s.%s' % (log_name1, log_name)
    # log.debug('log2_name: %s', log2_name)

    # log2 = logging.getLogger(log2_name)
    # log2.debug('xxxxxxxxxxxxxxxx, log2=%s, log2_name=%s', log2, log2_name)

    # log_name = get_logger_name(depth=2)
    # log_name = get_logger_name(depth=1)
    def wrapper(*args, **kwargs):
        # log_name = get_method_logger_name(depth=1)
        # print(get_logger_name())
        # print(get_logger_name(depth=2))
        # print('ga: %s' % getattr(wrapper, "__name__", None))
        qual_name = getattr(func, "__qualname__", None)
        func_name = qual_name or func.__name__
        # full_func_name = getattr(func, "__qualname__", '%s.%s' % (log_name, func.__name__))
        full_func_name = func_name or '%s.%s' % (log_name, func.__name__)

        log = logging.getLogger(log_name)
        log.debug('-- log_name=%s, log_name1=%s, log2_name=%s, qual_name=%s, func_name=%s, full_func_name=%s',
                  log_name, log_name1, log2_name, qual_name, func_name, full_func_name)
        log4_name = '%s.%s.%s' % (log_name1, log_name, func.__name__)
        log4 = get_logger(log4_name)

        # log4.debug('log4=%s', log4_name)
        # log.debug('t locals()=%s args=%s kwargs=%s', repr(locals()), repr(args), repr(kwargs))
        log4.debug('t locals()=%s args=%s kwargs=%s', repr(locals()), repr(args), repr(kwargs))

        log2 = get_class_logger(func, depth=1)
        # log2.debug('wrapper? %s', func_name)

        log3 = get_logger(func_name)
        # log3.debug('log_name=%s, log_name1=%s, log2_name=%s, logfunc_name=%s', log_name, log_name1, log2_name, func_name)

        try:
            ret = func(*args, **kwargs)
        except Exception as e:
            log.exception(e)
            raise

        log.debug('t ret=%s', repr(ret))
        log4.debug('t ret=%s', repr(ret))

        return ret

    return functools.update_wrapper(wrapper, func)


def setup(name=None, level=None, fmt=None, stream_formatter=None,
          file_formatter=None, use_root_logger=False, log_file=None):
    if name is None:
        name = 'alogging'

    use_multiprocessing = False

    fmt_string = fmt or os.environ.get('%s_fmt_string' % name, None)

    stream_formatter = stream_formatter or logging.Formatter(fmt=fmt_string)
    file_formatter = file_formatter or logging.Formatter(fmt=fmt_string)

    log = logging.getLogger(name)

    log.setLevel(level)

    log_file = log_file or os.path.expanduser('~/.alogging.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)

    stream_handler.setFormatter(stream_formatter)
    file_handler.setFormatter(file_formatter)

    log.addHandler(stream_handler)
    log.addHandler(file_handler)

    if use_multiprocessing:
        import multiprocessing
        mp_log = multiprocessing.get_logger()
        mp_log.setLevel(multiprocessing.SUBDEBUG)
        stream_handler.setLevel(multiprocessing.SUBDEBUG)
        mp_log.addHandler(stream_handler)

    if use_root_logger:
        setup_root_logger(root_level=logging.DEBUG)

    # import logging_tree
    # logging_tree.printout()

    return log


def setup_root_logger(root_level=None, handlers=None):
    if not handlers:
        handlers = [logging.NullHandler()]

    root_log_level = root_level or env_log_level('ROOT_LOG_LEVEL') or logging.INFO

    root_logger = logging.getLogger()
    root_logger.setLevel(root_log_level)

    for handler in handlers:
        root_logger.addHandler(handler)


def default_setup(name=None):
    # stream_fmt_string = """%(asctime)s %(name)s %(process)d %(funcName)s:%(lineno)d - %(message)s"""
    # stream_fmt_string = DEFAULT_STREAM_FMT_STRING
    stream_fmt_string = os.environ.get('%s_fmt_string' % name, None) or DEFAULT_STREAM_FMT_STRING
    # default_fmt_string = stream_fmt_string
    stream_datefmt_string = os.environ.get('%s_datefmt_string' % name, None) or DEFAULT_STREAM_DATEFMT_STRING
    stream_datefmt_string = "%H:%M:%S"
    stack_info = os.environ.get('ALOGGING_STACK_INFO', None) or STACK_INFO
    if stack_info:
        stream_fmt_string += STACK_INFO_FMT_STRING

    if HAS_COLOR_DEBUG:
        color_groups = [
                        ('funcName', ['funcName', 'lineno']),
                        ('levelname', ['levelno']),
                        ('name', ['stack_info']),
                        # ('name', ['filename', 'module',  'pathname']),
                        ('process', ['processName'])
        ]
        stream_formatter = color_debug.color_debug.ColorFormatter(fmt=stream_fmt_string,
                                                                  default_color_by_attr='name',
                                                                  # default_color_by_attr='process',
                                                                  auto_color=True,
                                                                  color_groups=color_groups,
                                                                  datefmt=stream_datefmt_string)
    else:
        stream_formatter = logging.Formatter(fmt=stream_fmt_string,
                                             datefmt=stream_datefmt_string)

    log_level = env_log_level('%s_log_level' % name) or logging.DEBUG

    return setup(name=name, level=log_level, fmt=DEFAULT_FMT_STRING, stream_formatter=stream_formatter,
                 use_root_logger=True)


# easier to remember alias
quickstart = default_setup


# From https://stackoverflow.com/a/47956089
def get_stack_size():
    """Get stack size for caller's frame.

    %timeit len(inspect.stack())
    8.86 ms +/- 42.5 us per loop (mean +/- std. dev. of 7 runs, 100 loops each)
    %timeit get_stack_size()
    4.17 us +/- 11.5 ns per loop (mean +/- std. dev. of 7 runs, 100000 loops each)
    """
    size = 2  # current frame and caller's frame always exist
    while True:
        try:
            sys._getframe(size)
            size += 1
        except ValueError:
            return size - 1  # subtract current frame
