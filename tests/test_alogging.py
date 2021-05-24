import logging

# from akl import alogging
import alogging
from alogging import t

import helpers

# yup, using the module under test to setup logging for its own tests
log = alogging.get_logger()

alogging.app_setup('')


def a_callable(foo=None):
    return b_callable(foo, ['bar'])


@alogging.t
def b_callable(foo=None, bar=None):
    # return '%s+%s' % (foo, bar)
    return foo + bar


def test_module_setup():
    log = alogging.module_setup('akl')
    log.debug('foo %s', 'blip', extra={'bar': 'baz'})


def test_get_logger_name():
    res = alogging.get_logger_name()
    assert res == 'test_alogging'


def test_get_logger():
    mlog = alogging.get_logger()
    log.debug('mlog: %s', mlog)

    mlog.debug('logging to test_alogging logger')


def test_get_method_logger_name():

    def some_inner_method(foo):
        meth_log = alogging.get_method_logger_name()

        return meth_log

    res_mlog = some_inner_method('blip')
    log.debug('res_mlog: %s', res_mlog)

    assert res_mlog == 'some_inner_method'


def test_get_method_logger():
    def another_inner_method(foo):
        meth_log = alogging.get_method_logger()

        return meth_log

    res_mlog = another_inner_method('blip')
    log.debug('res_mlog: %s', res_mlog)

    assert res_mlog == logging.getLogger('another_inner_method')


# TODO: paramaterize
def test_a():
    from alogging import a

    foo = {'blip': [1, 'two', 3.0, []]}

    res = a(foo)
    assert res == foo


def test_a_callable():
    things = [0, '', None, False, 1.1]
    exp_res = a_callable(foo=things)

    res = alogging.a(a_callable(foo=things))

    log.debug('exp_res: %s', exp_res)
    log.debug('res: %s', res)

    assert isinstance(res, list)
    assert 1.1 in res

    assert res == exp_res


def test_plain_t():
    from alogging import t

    @t
    def frob_the_swab_bar(foo, bar):
        return [bar, foo, '%s+++%s' % (foo, bar)]

    frob_the_swab_bar('javale', 'mcgee')


@t
class Stuff(object):
    thing = 1.1

    def __init__(self, a_color, mode=None):
        self.a_color = a_color
        self.bbb = 'beeeee'

    @t
    def add_color(self, b_color, opacity=None):
        return self.a_color + b_color


def test_t_class():
    stuff = Stuff('red', mode='chaos')
    new_color = stuff.add_color('green', opacity=91.1)
    log.debug('new_color: %s', new_color)


def test_t():
    from alogging import t

    # foo = {'blip': [1, 'two', 3.0, []]}

    @t
    def local_method(bar):
        return helpers.some_method(bar)

    res = local_method('expected')
    log.debug('res: %s', res)

    res = alogging.a(local_method('expected'))
    log.debug('res via a: %s', res)

    some_inst = helpers.SomeClass()
    res2 = some_inst.another_method('mmm', 'foobar')
    log.debug('res2: %s', res2)

    another_inst = helpers.AnotherClass('fOO')
    res3 = another_inst.blip()
    log.debug('res3: %s', res3)

    sub_inst = helpers.SubAnotherClass('SubF00')
    res4 = sub_inst.blip()
    log.debug('res4: %s', res4)

    @t
    def raise_exception():
        raise Exception('ttt')

    try:
        raise_exception()
    except Exception as e:
        log.debug(e)
        return

    assert False, 'expected an exception to be raised here'


def test_stack_info():
    alogging.STACK_INFO = True

    alogging.app_setup()
    slog = alogging.get_logger()

    def level_two(blip):
        slog.debug('some stuff, should include stack_info, blip=%s', blip)
        return blip

    def level_one(blip):
        slog.debug('alogging.STACK_INFO: %s', alogging.STACK_INFO)
        alogging.a(blip)
        return level_two(blip)

    resp = level_one('stuff')
    slog.debug('resp: %s', resp)

# def test_env_log_level():
#     with mock.patch('alogging.logger.os.environ', new={'FOO_LOG_LEVEL': 'DEBUG', 'BAR_LOG_LEVEL': 'sdfsdf'}) as me:
#         res = alogging.env_log_level('FOO_LOG_LEVEL')
#         log.debug('res: %s', res)
#         log.debug('me: %s', me)

#         try:
#             res = alogging.env_log_level('BAR_LOG_LEVEL')
#         except Exception as e:
#             log.exception(e)
#             return
#         log.debug('res: %s', res)
#         log.debug('me: %s', me)
#         assert False, 'Expected a Exception here for invalid log level'


def test_get_stack_size():
    res = alogging.get_stack_size()
    log.debug('res: %s', res)
