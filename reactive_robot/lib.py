"""
This module contains keywords to use it in robot scripts.
Contains shortcuts for common operations related to the Reactive Robot like getting payload,topic etc.
"""
import logging

from robot.api.deco import keyword
from robot.variables import variables

logger = logging.getLogger(__name__)


@keyword("Get Reactive Robot Payload")
def get_payload_as_dict() -> dict:
    logger.debug(variables)
    assert NotImplementedError


@keyword("Get Reactive Robot Topic")
def get_topic_as_str() -> str:
    logger.debug(variables)
    assert NotImplementedError
