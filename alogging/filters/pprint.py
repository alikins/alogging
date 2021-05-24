import collections
import logging
import pprint


class PprintArgsFilter(logging.Filter):
    '''Use pprint/pformat to pretty the log message args

    ie, log.debug("foo: %s", foo)
    this will pformat the value of the foo object.
    '''

    def __init__(self, name="", defaults=None):
        super(PprintArgsFilter, self).__init__(name=name)
        self.defaults = defaults or {}

    def filter(self, record):
        if not record.args:
            return True

        # Modify the log record in place, replacing the arg
        # with a pprint'ed version of it's values.

        # TODO: could wrap with a callable to defer evaluating
        #       the arg till the last minute
        # print("record.args1: %s" % list(record.args))

        # args can be a tuple or a dict/map, this bit is from logging.LogRecord.__init__
        args_map = {}
        if isinstance(record.args, collections.abc.Mapping):
            args_map = record.args

        if args_map:
            for arg, value in args_map.items():
                args_map[arg] = pprint.pformat(value)
            record.args = args_map
        else:
            record.args = tuple([pprint.pformat(x) for x in record.args])

        # record.args = tuple(pprint.pformat(x) for x in record.args)
        # print("record.args2: %s" % list(record.args))
        # for arg in record.args:
        #     print("arg: %s", arg)
        #     pretty_arg = pprint.pformat(record.args[arg])
        #     record.args[arg] = pretty_arg

        return True
