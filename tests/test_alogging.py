import logging
import mock

# from akl import alogging
import alogging

import helpers

# yup, using the module under test to setup logging for its own tests
log = alogging.get_logger()

alogging.default_setup('')


def test_log_setup():
    log = alogging.default_setup('akl')
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

    a(foo)


def test_t():
    from alogging import t

    # foo = {'blip': [1, 'two', 3.0, []]}

    @t
    def local_method(bar):
        return helpers.some_method(bar)

    res = local_method('expected')
    log.debug('res: %s', res)

    some_inst = helpers.SomeClass()
    res2 = some_inst.another_method('mmm', 'foobar')

    log.debug('res2: %s', res2)

    another_inst = helpers.AnotherClass('fOO')
    res3 = another_inst.blip()
    log.debug('res3: %s', res3)

    sub_inst = helpers.SubAnotherClass('SubF00')
    res4 = sub_inst.blip()

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

    alogging.default_setup()
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


def test_env_log_level():
    with mock.patch('alogging.os.environ', new={'FOO_LOG_LEVEL': 'DEBUG', 'BAR_LOG_LEVEL': 'sdfsdf'}) as me:
        res = alogging.env_log_level('FOO_LOG_LEVEL')
        log.debug('res: %s', res)
        log.debug('me: %s', me)

        try:
            res = alogging.env_log_level('BAR_LOG_LEVEL')
        except Exception as e:
            log.exception(e)
            return
        log.debug('res: %s', res)
        log.debug('me: %s', me)
        assert False, 'Expected a Exception here for invalid log level'


def test_get_stack_size():
    res = alogging.get_stack_size()
    log.debug('res: %s', res)

