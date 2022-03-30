import subprocess
import tempfile
from typing import Iterable, List
from urllib.parse import ParseResult

from kafka import KafkaConsumer

from reactive_robot.connectors.base import Connector
from reactive_robot.models import BindingModel
from reactive_robot.constants import EVENT_PAYLOAD_VARIABLE

import logging

logger = logging.getLogger("reactive_robot.connectors.kafka")


class KafkaConnector(Connector):

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
                    variables.append(f"${EVENT_PAYLOAD_VARIABLE}:${message.value.decode('utf-8')}")
                    self.executor.submit(self.run_robot, variables, b)
