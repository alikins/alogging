import sys

import alogging

from example import example_module

log = alogging.get_logger()


def main():
    # use some reasonable defaults for setting up logging.
    # - log to stderr
    # - use a default format:
    #   """%(asctime)s,%(msecs)03d %(levelname)-0.1s %(name)s %(processName)s:%(process)d %(funcName)s:%(lineno)d - %(message)s"""
    # main_log = alogging.default_setup(name='example.main')
    main_log = alogging.app_setup('example')
    main_log.debug('Log to logging "example.main"')

    example_module.do_startup_stuff()

    try:
        example_module.do_work()
    except Exception as exc:
        # gruntle a bit and continue
        log.exception(exc)

    log.debug('end of main')
    import logging_tree
    logging_tree.printout()


if __name__ == '__main__':
    log.debug('module scope of example.py started')
    sys.exit(main())
