import logging
import subprocess
import tempfile
from typing import List
from urllib.parse import ParseResult

import paho.mqtt.client as mqtt

from reactive_robot.connectors.base import Connector
from reactive_robot.models import BindingModel
from reactive_robot.parsers.string import RawPayloadParser

logger = logging.getLogger("reactive_robot.connectors.mqtt")


def _run_job(variables: List[str], binding: BindingModel):
    variable_cli = ["-v " + "".join(var) for var in variables]
    with tempfile.TemporaryDirectory() as tmpdirname:
        cmd = " ".join(["robot",
                        "--outputdir", tmpdirname,
                        " ".join(variable_cli),
                        binding.robot.file])

        logger.info("Executing cmd, %s" % cmd)
        subprocess.run(cmd.split(" "))


def _find_binding_by_topic(topic_name: str, bindings: List[BindingModel]):
    for b in bindings:
        if b.topic == topic_name:
            return b


class MQTTConnector(mqtt.Client, Connector):

    def __init__(self, *args, **kwargs):
        super(MQTTConnector, self).__init__(*args, **kwargs)

    def on_connect(self, mqttc, obj, flags, rc):
        logger.info("rc: " + str(rc) + "rc")

    def on_connect_fail(self, mqttc, obj):
        logger.error("MQTT broker connection failed")

    def on_message(self, mqttc, obj, msg):
        logger.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        binding = _find_binding_by_topic(msg.topic, self.bindings)
        parser = RawPayloadParser()
        self.executor.submit(_run_job, parser.get_variables(msg.payload), binding)

    def on_publish(self, mqttc, obj, mid):
        logger.debug("mid: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        logger.debug(string)

    def bind(self, connection_url: ParseResult, bindings=None):
        if bindings is None:
            bindings = []

        self.bindings = bindings
        logger.info(connection_url.hostname)
        logger.info(connection_url.port)
        self.connect(connection_url.hostname, connection_url.port, 60)

        for b in bindings:
            logger.info("%s -> subscribing topic: %s" % (b.name, b.topic))
            self.subscribe(b.topic)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc
