import logging

log = logging.getLogger(__name__)


def test_alogging_setup():
    from akl import alogging_setup  # noqa

    log.debug('blip')
