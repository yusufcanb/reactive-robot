import sys
from kafka import KafkaProducer
from multiprocessing import cpu_count

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers='kafka-broker:9092', )
    topic = sys.argv[-1]
    message_count = cpu_count() * 4
    for i in range(cpu_count() * 4):
        producer.send(topic, ('KAFKA_TOPIC=%s;TEST_VAR=%s' % (topic, i)).encode("UTF-8"))
        producer.flush()

    print("%s messages Sent to %s" % (message_count, topic))
