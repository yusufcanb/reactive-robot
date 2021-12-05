import asyncio
import logging
from importlib.metadata import import_module

from reactive_robot.exceptions import InjectionException

logger = logging.getLogger("reactive_robot.serve")


def serve(config):
    try:
        robot = import_module("robot")
        logger.info("Using Robot Framework v%s" % robot.version.get_full_version())
    except ImportError:
        logger.critical("Robot Framework not installed in active Python interpreter")
        raise InjectionException("Robot Framework not installed")

    try:
        module_name = config["connector"]["driver"].split(".")[:-1]
        cls_name = config["connector"]["driver"].split(".").pop()
        connector_cls = getattr(import_module(".".join(module_name)), cls_name)  # get class from module
    except ImportError:
        err_msg = "Failed to inject %s class" % config["connector"]["driver"]
        logger.critical(err_msg)
        raise InjectionException(err_msg)

    loop = asyncio.get_event_loop()
    connector = connector_cls()
    coroutine = loop.run_in_executor(None, lambda: connector.bind(loop=loop, bindings=config["bindings"]))

    logger.info("%s service started. Waiting for events." % config["service_name"])
    loop.run_until_complete(coroutine)

    loop.close()
