import logging
from abc import ABC, abstractmethod
from collections.abc import Iterable
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.parse import ParseResult

from reactive_robot.constants import MAX_WORKER
from reactive_robot.models import BindingModel
from reactive_robot.parsers.base import BaseParser

logger = logging.getLogger("reactive_robot.connectors.base")


class Connector(ABC):
    """
    Base class for connectors.
    Connectors are for handling to event source configurations.
    """

    bindings: Iterable[BindingModel]
    variable_parser: BaseParser
    executor = ThreadPoolExecutor(max_workers=MAX_WORKER)

    def __init__(self):
        logger.info("Thread executor initialized with %s workers" % MAX_WORKER)

    @abstractmethod
    def bind(self, connection_url: ParseResult, bindings: Iterable[BindingModel]):
        raise NotImplemented
