import subprocess
import tempfile
from typing import Iterable, List
from urllib.parse import ParseResult

from kafka import KafkaConsumer

from reactive_robot.connectors.base import Connector
from reactive_robot.models import BindingModel

import logging

logger = logging.getLogger("reactive_robot.connectors.kafka")


class KafkaConnector(Connector):

    def _run_job(self, variables: List[str], binding: BindingModel):
        variable_cli = ["-v " + "".join(var) for var in variables]
        with tempfile.TemporaryDirectory() as tmpdirname:
            cmd = " ".join(["robot",
                            "--outputdir", tmpdirname,
                            " ".join(variable_cli),
                            binding.robot.file])

            logger.debug("Executing cmd, %s" % cmd)
            subprocess.run(cmd.split(" "))

    def bind(self, connection_url: ParseResult, bindings: Iterable[BindingModel], **kwargs):
        consumer = KafkaConsumer(group_id=kwargs.get("group_id", "reactive-robot"),
                                 bootstrap_servers=connection_url.netloc)
        consumer.subscribe(topics=[b.topic for b in bindings])

        for message in consumer:
            if self.variable_parser is not None:
                variables = []
            else:
                variables = []

            for b in bindings:
                if b.topic == message.topic:
                    variables.append("REACTIVE_ROBOT_RECEIVED_MSG:%s" % message.value.decode("utf-8"))
                    self.executor.submit(self._run_job, variables, b)
