import logging

from akl import pp, pf

log = logging.getLogger(__name__)


BAR = {'blip': 'baz'}

class Foo(object):
    class_baz = 'baz'

    def __init__(self, blip=None):
        self.blip = blip
        self._stuff = 'dunderstuff'
        self._more_stuff = 'dundermorestuff'

    @property
    def stuff(self):
        return self._stuff


def test_pf_dict():
    res = pf(BAR)

    log.debug('res: %s', res)


def test_pf_object():
    obj = Foo('random crap')

    res = pf(obj)

    log.debug('res: %s', res)


def test_pp_dict():
    pp(BAR)


def test_pp_object():
    obj = Foo('random pp stuff')
    pp(obj)
