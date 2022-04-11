import click
import logging

from colorlog import ColoredFormatter


class Log(object):
    """
    Maintain logging level
    """

    format = "%(log_color)s[%(asctime)s] - %(levelname)-s%(reset)s - %(log_color)s%(message)s%(reset)s"

    def __init__(self, log_name="reactive_robot", level=logging.INFO):
        self.logger = logging.getLogger(log_name)

        self.logger.setLevel(1)
        self.logger.propagate = False

        self.stream = logging.StreamHandler()
        self.stream.setLevel(level)
        self.stream.setFormatter(ColoredFormatter(self.format))

        self.stream.name = "RxRobotStreamHandler"
        self.logger.addHandler(self.stream)
