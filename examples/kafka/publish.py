from kafka import KafkaProducer
from multiprocessing import cpu_count

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers='kafka:9092', )
    topic = "robot.hw"
    for i in range(cpu_count() * 4):
        producer.send(topic, ('KAFKA_TOPIC=%s;TEST_VAR=%s' % (topic, i)).encode("UTF-8"))
        producer.flush()
