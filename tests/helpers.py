import alogging


@alogging.t
def some_method(blip):
    return blip


class SomeClass(object):
    @alogging.t
    def some_method(self, bar):
        fizz = 'Fizz'
        if fizz and bar:
            return bar
        return bar

    @alogging.t
    def another_method(self, bar, arg2):
        if arg2 == 'whatever':
            return None
        return self.some_method(bar)


class AnotherClass(object):
    def __init__(self, foo):
        self.foo = foo
        self.log = alogging.get_class_logger(self)
        self.log.debug('init')

    def blip(self):
        return 'BLIP%sBLIP' % self.foo


class SubAnotherClass(AnotherClass):
    @alogging.t
    def blip(self):
        self.log.info('blipping')
        return super(SubAnotherClass, self).blip()
