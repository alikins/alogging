import logging
import pprint


class PPrintRecordFormatter(logging.Formatter):
    '''Pretty print the __dict__ of the log record.'''
    def __init__(self, fmt=None, datefmt=None, indent=1, style='%'):
        super(PPrintRecordFormatter, self).__init__(fmt=fmt,
                                                    datefmt=datefmt,
                                                    style=style)

        self.indent = indent

    def format(self, record):
        res_dict = record.__dict__.copy()
        message = record.getMessage()
        res_dict['message'] = message
        rendered = super().format(record)
        res = '\n'.join([rendered,
                         pprint.pformat(res_dict, indent=self.indent)])
        return res

    def __repr__(self):
        buf = '%s(fmt="%s", indent=%s, style=%s)' % (self.__class__.__name__,
                                                     self._fmt,
                                                     self.indent,
                                                     self._style)
        return buf
