import asyncio
import logging
from importlib.metadata import import_module

import aio_pika

logger = logging.getLogger("reactive_robot.serve")


async def run_task(connection, topic=None, robot=None, **kwargs):
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(topic, auto_delete=False, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                logger.info("Received message headers: %s, body: %s " % (message.headers, str(message.body)))
                logger.info("%s will be executed with args: %s", robot["file"], robot["args"])
                async with message.process():
                    robotframework = import_module("robot")
                    robotframework.run(robot["file"])


async def main(loop, connection_url, bindings=None):
    if bindings is None:
        bindings = []

    connection = await aio_pika.connect_robust(connection_url, loop=loop)

    tasks = []
    for binding in bindings:
        tasks.append(run_task(connection, **binding))

    await asyncio.wait(tasks)


def serve(config):
    try:
        robot = import_module("robot")
        logger.info("Using Robot Framework v%s" % robot.version.get_full_version())
    except ImportError:
        logger.error("Robot Framework not installed in active Python interpreter")
        raise Exception("Robot Framework not installed")

    connector_module = config["connector"]["driver"].split(".")[:-1]
    connector_cls = config["connector"]["driver"].split(".").pop()
    try:
        Klass = getattr(import_module(".".join(connector_module)), connector_cls)
        connector = Klass()
    except ImportError:
        logger.error("Failed to inject %s class" % config["connector"]["driver"])
        raise Exception("Failed to inject %s class" % config["connector"]["driver"])

    connector.configure()

    loop = asyncio.get_event_loop()

    coroutine = loop.run_in_executor(None, lambda: connector.run())
    logger.info("%s service started. Waiting for events." % config["service_name"])
    loop.run_until_complete(coroutine)

    loop.close()
