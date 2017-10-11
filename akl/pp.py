import pprint


def pf(obj):
    if hasattr(obj, '__dict__'):
        return pprint.pformat(obj.__dict__)


def pp(obj):
    print(pf(obj))
