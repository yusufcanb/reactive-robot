import asyncio
import logging
from importlib.metadata import import_module

import aio_pika

from reactive_robot.connectors.base import Connector

logger = logging.getLogger("connectors.rabbitmq")


class RabbitMqConnector(Connector):
    """
    RabbitMQ connector for handling events via RabbitMQ queues.
    """

    async def run_task(self, connection, topic=None, robot=None, **kwargs):
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(topic, auto_delete=True)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    logger.info("Received message headers: %s, body: %s " % (message.headers, str(message.body)))
                    logger.info("%s will be executed with args: %s", robot["file"], robot["args"])
                    async with message.process():
                        robotframework = import_module("robot")
                        robotframework.run(robot["file"])

        async def main(self, loop, connection_url, bindings=None):
            if bindings is None:
                bindings = []

            connection = await aio_pika.connect_robust(connection_url, loop=loop)

            tasks = []
            for binding in bindings:
                tasks.append(self.run_task(connection, **binding))

            await asyncio.wait(tasks)

    def serve(config):
        try:
            robot = import_module("robot")
            logger.info("Using Robot Framework v%s" % robot.version.get_full_version())
        except ImportError:
            logger.error("Robot Framework not installed in active Python interpreter")
            raise Exception("Robot Framework not installed")

        loop = asyncio.get_event_loop()

        logger.info("Event loop started. Waiting for events.")
        # loop.run_until_complete(main(loop, config["connector"]["connection_url"], config["bindings"]))

        loop.close()

    def bind(self, loop, bindings):
        pass
