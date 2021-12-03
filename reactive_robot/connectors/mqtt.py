import asyncio

import paho.mqtt.client as mqtt

from .base import Connector


class MyMQTTClass(Connector, mqtt.Client):
    channel: str

    def __init__(self, channel="$SYS/#"):
        self.channel = channel
        super(MyMQTTClass, self).__init__()

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: " + str(rc))

    def on_connect_fail(self, mqttc, obj):
        print("Connect failed")

    def on_message(self, mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("mid: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def configure(self):
        self.connect("localhost", 1883, 60)

    def run(self):
        self.subscribe("python/mqtt/1")

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    mqttc = MyMQTTClass("python/mqtt/1")
    coroutine = loop.run_in_executor(None, lambda: mqttc.run())
    loop.run_until_complete(coroutine)
