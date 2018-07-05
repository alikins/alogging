import logging

log = logging.getLogger(__name__)


def test_alogging_setup():
    from alogging import alogging_setup  # noqa

    log.debug('blip')
