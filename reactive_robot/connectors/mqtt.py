import logging
from urllib.parse import ParseResult

import paho.mqtt.client as mqtt

from reactive_robot.connectors.base import Connector
from reactive_robot.constants import EVENT_PAYLOAD_VARIABLE, EVENT_TOPIC_VARIABLE

logger = logging.getLogger("reactive_robot.connectors.mqtt")


class MQTTConnector(mqtt.Client, Connector):
    def __init__(self, *args, **kwargs):
        super(MQTTConnector, self).__init__(*args, **kwargs)

    def _has_wildcard(self, topic: str):
        return "+" in topic or "#" in topic

    def on_connect(self, mqttc, obj, flags, rc):
        logger.info("rc: " + str(rc) + "rc")

    def on_connect_fail(self, mqttc, obj):
        logger.error("MQTT broker connection failed")

    def on_message(self, mqttc, obj, msg):
        logger.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        binding = self.find_binding_by_topic(msg.topic)
        if self.variable_parser is not None:
            variables = []
        else:
            variables = []
        variables.append(f"{EVENT_PAYLOAD_VARIABLE}:{self.encode_payload_to_base64(msg.payload)}")
        variables.append(f"{EVENT_TOPIC_VARIABLE}:{msg.topic}")
        self.executor.submit(self.run_robot, variables, binding)

    def on_publish(self, mqttc, obj, mid):
        logger.debug("mid: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        logger.debug(string)

    def bind(self, connection_url: ParseResult, bindings=None, **kwargs):
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
