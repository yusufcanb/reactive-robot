from abc import ABC, abstractmethod


class Connector(ABC):
    """
    Base class for connectors.
    Connectors are for handling to event source configurations.
    """

    @abstractmethod
    def configure(self):
        raise NotImplemented()

    @abstractmethod
    def run(self):
        raise NotImplemented()
