# Reactive Robot (⚡️🤖)

<!-- ![pypi-badge](https://img.shields.io/pypi/v/reactive-robot) -->

![stable](https://img.shields.io/static/v1?label=status&message=alpha-phase&color=yellow)

## Mission

This project aims to turning Robot Framework projects into event-driven services using popular message brokers like RabbitMQ, Kafka or MQTT.

## Usage

Create a definiton file called `reactive-robot.yml` then paste following configuration;

```yaml

service_name: Example Robot Service
service_version: 1.0.0

connector:
  driver: reactive_robot.connectors.rabbitmq.RabbitMQConnector
  connection_url: amqp://guest:guest@localhost:5672

bindings:
  - name: Example Task
    topic: robot-queue
    robot:
      file: your-robots/example.robot
      args: null
```

You're all set!
Now all you have to do is start the service;

```
python -m reactive_robot serve
```

You should see the following output;

```
$ python -m reactive_robot serve
2021-11-27 18:22:58,517 - [INFO] - reactive_robot.serve::serve::40 - Using Robot Framework v4.1.2 (Python 3.10.0 on darwin)
2021-11-27 18:22:58,518 - [INFO] - reactive_robot.serve::serve::47 - Event loop started. Waiting for events.
```



