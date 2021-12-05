from abc import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    def get_variables(self, message: bytes):
        raise NotImplementedError("Method not implemented")
