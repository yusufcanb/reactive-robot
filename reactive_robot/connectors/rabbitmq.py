import subprocess
import tempfile
import pika

from typing import Iterable
from urllib.parse import ParseResult

from reactive_robot.connectors.base import Connector
from reactive_robot.models import BindingModel

import logging

logger = logging.getLogger("reactive_robot.connectors.rabbitmq")


class RabbitMQConnector(Connector):

    def _map_binding(self, channel, binding: BindingModel):
        channel.exchange_declare(exchange=binding.topic, exchange_type='fanout')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=binding.topic, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=self.on_message, auto_ack=True)

    def on_message(self, ch, method, properties, body):
        logger.info("Received message %s from channel %s" % (body, method.exchange))
        self.executor.submit(lambda: self.run_robot(method.exchange, body))

    def bind(self, connection_url: ParseResult, bindings: Iterable[BindingModel]):
        connection = pika.BlockingConnection(pika.URLParameters(connection_url.geturl()))
        self.bindings = bindings

        channel = connection.channel()
        for binding in bindings:
            self._map_binding(channel, binding)

        channel.start_consuming()
