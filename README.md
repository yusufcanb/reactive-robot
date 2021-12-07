# Reactive Robot (⚡ 🤖)

<!-- ![pypi-badge](https://img.shields.io/pypi/v/reactive-robot) -->

![stable](https://img.shields.io/static/v1?label=status&message=alpha-phase&color=yellow)

## Mission

This project aims to turn Robot Framework projects into event-driven services using popular message brokers like RabbitMQ, Kafka or MQTT.

## Usage

Create a definition file called `reactive-robot.yml` then paste following configuration;

```yaml

service_name: Example Robot Service
service_version: 1.0.0

connector:
  driver: reactive_robot.connectors.mqtt.MQTTConnector
  connection_url: mqtt://localhost:1883

bindings:
  - name: Example Task
    topic: robot-queue
    robot:
      file: your-robots/examples.robot
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

Finally publish a message to see your robots are running.

```
python tests/mqtt/publish.py localhost 1883
```
## Examples

### Robot Service with MQTT Broker

```
cd examples/mqtt
docker-compose up
```

## Recipes

In the [examples/](examples) directory you can find example projects which implements all recipes below;

### Dockerize your service

Here you can find an example Dockerfile to convert your Robot Framework projects into dockerized event-driven service 

```dockerfile
FROM robotframework/rfdocker

WORKDIR /opt/service

COPY . /opt/service
RUN pip install -r requirements.txt  # Your project dependencies.

# reactive-robot setup
COPY reactive-robot.yml .
RUN pip install reactive-robot

CMD ["python", "-m", "reactive-robot", "serve"]
```

Then, we can build the image with following;

```
docker build -t robot-service:1.0.0 .
```

Finally, run your service;

```
docker run -it robot-service:1.0.0
```


## License

Distributed under the Apache License 2.
See `LICENSE` for more information.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create.
Any contributions are **appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/some-feature`)
3. Commit your Changes (`git commit -m 'some feature added'`)
4. Push to the Branch (`git push origin feature/some-feature`)
5. Open a Pull Request
