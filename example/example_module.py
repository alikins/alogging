import alogging

# local alias for alogging.a()
a = alogging.a

log = alogging.get_logger()


class ThingToDo(object):
    def __init__(self, requirement, priority=None, assigner=None):
        # get a Logger named 'example.ThingToDo'
        self.log = alogging.get_class_logger(self)

        self.log.info('Task as assigned: req=%s, pri=%s, ass=%s', requirement, priority, assigner)

        priority = priority or 'never'

        self.log.info('Task reprioritized: req=%s, pri=%s, ass=%s', requirement, priority, assigner)


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
    # has_coffee = a(find_coffee(coffee_places))
    has_coffee = find_coffee(a(coffee_places))

    log.warning('No coffee found, there is no hope now... has_coffee=%s', has_coffee)

    work_accomplished = space_out_for_while(duration=300)

    log.debug('work_acomplished: %s', work_accomplished)


def do_work():
    next_task = ThingToDo('finish TODO list', assigner='Lumberg')
    if not next_task:
        return

    # oh no, work...
    log.error("I'm slammed at the moment, I can't do %s", next_task)
    raise Exception()
