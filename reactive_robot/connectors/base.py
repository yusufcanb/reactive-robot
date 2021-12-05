from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from collections.abc import Iterable

from reactive_robot.bindings import AbstractBinding


class Connector(ABC):
    """
    Base class for connectors.
    Connectors are for handling to event source configurations.
    """

    event_loop: AbstractEventLoop
    bindings: Iterable[AbstractBinding]

    def __init__(self, loop=None, bindings=None):
        self.event_loop = loop
        self.bindings = bindings

    @abstractmethod
    def bind(self, loop: AbstractEventLoop, bindings: Iterable[AbstractBinding]):
        raise NotImplemented
