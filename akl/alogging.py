
import inspect
import logging
import os

HAS_COLOR_DEBUG = False
try:
    # https://github.com/alikins/color_debug
    import color_debug
    HAS_COLOR_DEBUG = True
except ImportError as e:
    print(e)

DEFAULT_FMT_STRING = """%(asctime)s %(name)s %(process)d %(funcName)s:%(lineno)d - %(message)s"""
DEFAULT_FILE_FMT_STRING = DEFAULT_STREAM_FMT_STRING = DEFAULT_FMT_STRING


# TODO: add a stack depth indicator filter?
#       filter would expect 'extra' to have a 'stack_depth' int attribute
#       The filter would replace value of 'stack_depth' with a string that
#       is basically '.' * stack_depth.
#       That adds a visual indicator to log lines about the stack depth

def env_log_level(var_name):

    # be liberal in log env var name cap
    for env_var_candidates in (var_name, var_name.upper(), var_name.lower()):
        env_var_value = os.environ.get(var_name, None)
        if env_var_value is not None:
            continue

    print('%s=%s' % (var_name, env_var_value))

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


def get_logger():
    '''Use to get a logger with name of callers __name__

    Can be used in place of:

        import logging
        log = logging.getLogger(__name__)

    That can be replaced with

        from akl import alogging
        log = alogging.get_logger()
    '''
    return logging.getLogger(get_logger_name(depth=2))


def get_class_logger(obj):
    '''Use to get a logger with name equiv to module.Class

    in a regular class __init__, use like:

        self.log = alogging.get_class_logger(self)


    In a metaclass __new__, use like:

        log = alogging.get_class_logger(cls)
    '''

    return logging.getLogger(get_class_logger_name(obj, depth=2))


def get_method_logger():
    return logging.getLogger(get_method_logger_name(depth=2))


def setup(name=None, level=None, fmt=None, stream_formatter=None, file_formatter=None, use_root_logger=False, log_file=None):
    name = name or 'akl'

    use_multiprocessing = False

    fmt_string = fmt or os.environ.get('%s_fmt_string' % name, None)

    stream_formatter = stream_formatter or logging.Formatter(fmt=fmt_string)
    file_formatter = file_formatter or logging.Formatter(fmt=fmt_string)

    null_handler = logging.NullHandler()

    log_level = level or env_log_level('%s_log_level' % name) or logging.DEBUG

    log = logging.getLogger(name)

    log.setLevel(log_level)

    log_file = log_file or os.path.expanduser('~/.akl.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

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
                          # handlers=[stream_handler, file_handler, null_handler])


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

    # fmt = '%(asctime)s processName:%(processName)s process:%(process)d threadName '
    # '%(threadName)-2s level: %(levelname)s module: %(module)s name: %(name)s '
    # 'funcName: %(funcName)s lineno: %(lineno)d %(message)s'

    # fmt_all = '%(asctime)s %(levelname)-0.1s %(levelno)-0.1d %(processName)-0.1s '
    # '%(process)d %(threadName)s %(thread)d %(name)s %(module)s %(filename)s %(lineno)d - %(message)s'
    # stream_fmt_string = stream_fmt_string

    if HAS_COLOR_DEBUG:
        color_groups = [
                        ('funcName', ['funcName', 'lineno']),
                        # ('name', ['filename', 'module',  'pathname']),
                        ('process', ['processName'])]
        stream_formatter = color_debug.color_debug.ColorFormatter(fmt=stream_fmt_string,
                                                                  default_color_by_attr='name',
                                                                  color_groups=color_groups)
    else:
        stream_formatter = logging.Formatter(fmt=stream_fmt_string)

    setup(name=name, level=logging.DEBUG, fmt=DEFAULT_FMT_STRING, stream_formatter=stream_formatter,
          use_root_logger=True)

    import logging_tree
    logging_tree.printout()
