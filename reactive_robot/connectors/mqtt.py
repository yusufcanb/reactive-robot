import logging
from urllib.parse import ParseResult

import paho.mqtt.client as mqtt

from reactive_robot.connectors.base import Connector
from reactive_robot.constants import EVENT_PAYLOAD_VARIABLE, EVENT_TOPIC_VARIABLE

logger = logging.getLogger("reactive_robot.connectors.mqtt")


class MqttTopic(object):
    topic: str

    def __init__(self, topic: str) -> None:
        self.topic = topic

    def __eq__(self, mqtt_topic: any) -> bool:
        if not isinstance(mqtt_topic, MqttTopic):
            return False

        if self.has_wild_card() is False and mqtt_topic.has_wild_card() is False:
            return self.topic == mqtt_topic.topic

        if self.has_plus_sign() or mqtt_topic.has_plus_sign():
            if len(self.as_arr()) != len(mqtt_topic.as_arr()):
                return False
            for i in range(len(self.topic.split("/"))):
                if self.as_arr()[i] == mqtt_topic.as_arr()[i]:
                    continue
                elif self.as_arr()[i] == "+" or mqtt_topic.as_arr()[i] == "+":
                    continue
                else:
                    return False
            return True

        if self.has_sharp_sign() or mqtt_topic.has_sharp_sign():
            if self.has_sharp_sign():
                t1 = self.topic.replace("#", "")
                t2 = mqtt_topic.topic
            else:
                t1 = mqtt_topic.topic.replace("#", "")
                t2 = self.topic

            if t1 in t2:
                return True
        return False

    def has_plus_sign(self):
        return "+" in self.topic

    def has_sharp_sign(self):
        return "#" in self.topic

    def has_wild_card(self) -> bool:
        return self.has_plus_sign() or self.has_sharp_sign()

    def __repr__(self) -> str:
        return self.topic

    def __str__(self) -> str:
        return self.__repr__()

    def as_arr(self) -> list:
        return self.topic.split("/")


class MQTTConnector(mqtt.Client, Connector):
    def __init__(self, *args, **kwargs):
        super(MQTTConnector, self).__init__(*args, **kwargs)

    def on_connect(self, mqttc, obj, flags, rc):
        logger.info("rc: " + str(rc) + "rc")

    def on_connect_fail(self, mqttc, obj):
        logger.error("MQTT broker connection failed")

    def on_message(self, mqttc, obj, msg):
        logger.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        binding = self.find_binding_by_topic(MqttTopic(msg.topic))
        if self.variable_parser is not None:
            variables = []
        else:
            variables = []
        variables.append(
            f"{EVENT_PAYLOAD_VARIABLE}:{self.encode_payload_to_base64(msg.payload)}"
        )
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

        for binding in bindings:
            binding.topic = MqttTopic(binding.topic)
        self.bindings = bindings

        logger.info(connection_url.hostname)
        logger.info(connection_url.port)
        self.connect(connection_url.hostname, connection_url.port, 60)

        for b in self.bindings:
            logger.info("%s -> subscribing topic: %s" % (b.name, b.topic.__str__()))
            self.subscribe(b.topic.__str__())

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc
