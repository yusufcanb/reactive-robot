"""
This module contains keywords to use it in robot scripts.
Contains shortcuts for common operations related to the Reactive Robot like getting payload,topic etc.
"""
import base64
import logging

from robot.api.deco import keyword
from robot.running import EXECUTION_CONTEXTS

from reactive_robot.constants import EVENT_TOPIC_VARIABLE, EVENT_PAYLOAD_VARIABLE

logger = logging.getLogger(__name__)


@keyword("Get Reactive Robot Payload")
def get_payload_as_dict() -> dict:
    context = EXECUTION_CONTEXTS.top
    variables = context.variables.current.store
    return  base64.b64decode(variables.data[EVENT_PAYLOAD_VARIABLE])


@keyword("Get Reactive Robot Topic")
def get_topic_as_str() -> str:
    context = EXECUTION_CONTEXTS.top
    variables = context.variables.current.store
    return variables.data[EVENT_TOPIC_VARIABLE]
