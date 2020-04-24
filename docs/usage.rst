=====
Usage
=====

To use alogging in a project::

    import alogging

Examples
--------

Basic use of alogging::

    import alogging

    # local alias for alogging.a()
    a = alogging.a

    # create a logging.Logger object, will use the __name__ of the
    # module by default. Equilivent to 'log = logging.getLogger(__name__)'
    log = alogging.get_logger()

    log.debug('created a Logger object so use it for a debug msg')


    class ThingToDo(object):
        def __init__(self, requirement, priority=None, assigner=None):
            # get a Logger named 'example.ThingToDo'
            self.log = alogging.get_class_logger(self)

            self.log.info('Task as assigned: req=%s, pri=%s, ass=%s', requirement, priority, assigner)

            priority = priority or 'never'

            self.log.info('Task reprioritized: req=%s, pri=%s, ass=%s', requirement, priority, assigner')


    # alogging.t decorator will log when the decorated method is called,
    # what args it was passed, and what it's return value was

    @alogging.t
    def space_out_for_while(duration=None):
        # space out for 10 minutes by default
        duration = duration or 600

        # return the total amount of work accomplished
        return 0

    def find_coffee(coffee_places):
        log.debug('looking for coffee')
        return None

    def do_startup_stuff():
        coffee_places = ['piehole', 'mug_on_desk', 'coffee_machine', 'krankies']
        # log the the args to find_coffee as it is called
        has_coffee = a(find_coffee(coffee_places))

        work_accomplished = space_out_for_while(duration=300)

    def do_work():
        next_task = TaskToDo('finish TODO list', assigner='Lumberg')
        if not next_task:
            return

        # oh no, work...
        log.error("I'm slammed at the moment, I can't do %s', next_task)
        raise Exception()

    if __name__ = '__main__':
        # use some reasonable defaults for setting up logging.
        # - log to stderr
        # - use a default format:
        #   """%(asctime)s,%(msecs)03d %(levelname)-0.1s %(name)s %(processName)s:%(process)d %(funcName)s:%(lineno)d - %(message)s"""
        main_log = alogging.default_setup(name='example.main')
        main_log.debug('Log to logging "example.main"')

        do_startup_stuff()

        try:
            do_work()
        except Exception as exc:
            # gruntle a bit and continue
            log.exception(exc)

Another Example
---------------

Example uses of alogger::

    # color almost everything by logger name
    color_groups = [('name', ['filename', 'module', 'lineno', 'funcName', 'pathname'])]

