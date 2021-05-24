import logging

# TODO: include support for regex based excludes as well


class ExcludeFilter(logging.Filter):
    '''Filter records with user provided values for record fields

    ie, to exclude log records from loop polling records from
    the 'asyncio' module, with name='asyncio', module='base_events',
    func_name='_run_once'
    '''

    def __init__(self, name="", excludes=None, operator=None):
        '''excludes is a list of tuples (field_name, value)'''
        super(ExcludeFilter, self).__init__(name=name)
        self.excludes = excludes or []

        operators = {'ALL': all,
                     'ANY': any}
        # TODO: try/except
        operator = operator or "ALL"
        operator = str(operator).upper()
        self.operator = operators.get(operator, all)

    def filter(self, record):
        # Don't exclude anything if given no excludes
        if not self.excludes:
            return True
        checks = [self.check_value(field_name, value, record) for (field_name, value) in self.excludes]
        # ~ any() or all()
        return not self.operator(checks)

    def check_value(self, field_name, value, record):
        if hasattr(record, field_name):
            if getattr(record, field_name) == value:
                return True
        return False

    def __repr__(self):
        return f"{__name__}.{self.__class__.__name__}(excludes={self.excludes}, operator={self.operator})"
