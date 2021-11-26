import logging


class Log(object):
    """
    Maintain logging level
    """

    def __init__(self, log_name='rx_robot', level=logging.INFO):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(1)
        self.logger.propagate = False

        self.stream = logging.StreamHandler()
        self.stream.setLevel(level)
        self.stream.setFormatter(
            logging.Formatter(fmt='%(asctime)s - [%(levelname)s] - %(name)s::%(funcName)s - %(message)s'))

        self.stream.name = 'RxRobotStreamHandler'
        self.logger.addHandler(self.stream)
