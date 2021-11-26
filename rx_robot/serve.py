import asyncio
import aio_pika
import logging

from importlib.metadata import import_module

logger = logging.getLogger("rx_robot.serve")


async def run_task(connection, queue_name=None):
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                logger.info("Received message headers: %s, body: %s " % (message.headers, str(message.body)))
                async with message.process():
                    robot = import_module("robot")
                    robot.run("tests/robots/basic.robot")


async def main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@localhost:5672", loop=loop
    )

    binding1 = run_task(connection, queue_name="1")
    binding2 = run_task(connection, queue_name="2")
    binding3 = run_task(connection, queue_name="3")
    binding4 = run_task(connection, queue_name="robot_queue_2")

    await asyncio.wait([binding1, binding2, binding3, binding4])


def serve(config):
    try:
        robot = import_module("robot")
        logger.info("Using Robot Framework v%s" % robot.version.get_full_version())
    except ImportError:
        logger.error("Robot Framework not installed in active Python interpreter")
        raise Exception("Robot Framework not installed")

    loop = asyncio.get_event_loop()

    logger.info("Event loop started. Waiting for events.")
    loop.run_until_complete(main(loop))

    loop.close()
