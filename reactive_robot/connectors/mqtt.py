import logging
import time

import paho.mqtt.client as mqtt

from .base import Connector

logger = logging.getLogger("reactive_robot.connectors.mqtt")


class MQTTConnector(mqtt.Client, Connector):

    def __init__(self, *args, **kwargs):
        super(MQTTConnector, self).__init__(*args, **kwargs)

    def on_connect(self, mqttc, obj, flags, rc):
        logger.info("rc: " + str(rc) + "rc")

    def on_connect_fail(self, mqttc, obj):
        logger.error("MQTT broker connection failed")

    def on_message(self, mqttc, obj, msg):
        logger.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        from robot import run, run_cli
        self.event_loop.run_in_executor(None, lambda: run_cli(
            ["--name", time.time(), "--outputdir", ".output/%s" % time.time(), "tests/robots/http.robot"]))

    def on_publish(self, mqttc, obj, mid):
        logger.debug("mid: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        logger.debug(string)

    def bind(self, loop=None, bindings=None):
        self.event_loop = loop
        self.bindings = bindings

        self.connect("localhost", 1883, 60)
        self.subscribe("hello-world")

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc


if __name__ == "__main__":
    mqttc = MQTTConnector()
    mqttc.run()
