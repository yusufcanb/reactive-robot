from reactive_robot.parsers.base import BaseParser


class RawPayloadParser(BaseParser):

    def get_variables(self, message: bytes):
        if message:
            variables = message.decode("utf-8").split()
            return variables
        else:
            return []
