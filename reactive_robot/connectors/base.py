import subprocess
import logging
import tempfile
import base64

from typing import List
from abc import ABC, abstractmethod
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

    bindings: List[BindingModel]
    variable_parser: BaseParser
    executor = ThreadPoolExecutor(max_workers=MAX_WORKER)

    def __init__(self):
        logger.info("Thread executor initialized with %s workers" % MAX_WORKER)

    def encode_payload_to_base64(self, payload: bytes) -> str:
        """
        Convert incoming payload to base64 string to avoid security risks.
        """
        return base64.b64encode(payload).decode("utf-8")

    def run_robot(self, variables: List[str], binding: BindingModel):
        variable_cli = ["-v " + "".join(var) for var in variables]
        with tempfile.TemporaryDirectory() as tmpdirname:
            cmd = " ".join(
                [
                    "robot",
                    binding.robot.args
                    if binding.robot.args
                    else f"--outputdir {tmpdirname}",
                    " ".join(variable_cli),
                    binding.robot.file,
                ]
            )
            logger.info("Executing cmd, %s" % cmd)
            subprocess.run(cmd.split(" "))

    def find_binding_by_topic(self, topic_name: str):
        for b in self.bindings:
            if b.topic == topic_name:
                logger.debug(
                    "Topic [%s] matched with binding [%s]" % (topic_name, b.name)
                )
                return b
        logger.error("No binding matched for topic [%s], skipping" % topic_name)

    @abstractmethod
    def bind(self, connection_url: ParseResult, bindings: List[BindingModel], **kwargs):
        raise NotImplementedError
