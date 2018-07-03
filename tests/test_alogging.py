import logging

from akl import alogging

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
    from akl.alogging import a

    foo = {'blip': [1, 'two', 3.0, []]}

    a(foo)


def test_t():
    from akl.alogging import t

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

    import logging_tree
    logging_tree.printout()
