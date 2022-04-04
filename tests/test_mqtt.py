from reactive_robot.connectors.mqtt import MqttTopic


def test_mqtt_topic_has_wilcard():
    topic1 = MqttTopic("device/+/temperture")
    assert topic1.has_wild_card() == True

    topic2 = MqttTopic("device/#")
    assert topic2.has_wild_card() == True

    topic2 = MqttTopic("device/a42b4d93/temperture")
    assert topic2.has_wild_card() == False


def test_mqtt_topics_are_equals():
    topic1 = MqttTopic("device/abcdd12/temperture")
    topic2 = MqttTopic("device/abcdd12/temperture")

    assert (topic1 == topic2) is True

    topic1 = MqttTopic("device/+/temperture/+/value")
    topic2 = MqttTopic("device/abcdd12/temperture/1/value")

    assert (topic1 == topic2) is True

    topic1 = MqttTopic("device/#")
    topic2 = MqttTopic("device/asbdf/temperture/r23r")
    topic3 = MqttTopic("device/asbdf/coordinate")

    assert (topic1 == topic2) is True
    assert (topic1 == topic3) is True
    assert (topic2 == topic3) is False
