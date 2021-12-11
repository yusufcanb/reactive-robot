import asyncio
import logging
from importlib.metadata import import_module

from reactive_robot.exceptions import InjectionException
from reactive_robot.models import ReactiveRobotModel

logger = logging.getLogger("reactive_robot.serve")


def _check_robot_exists():
    try:
        robot = import_module("robot")
        logger.info("Using Robot Framework v%s" % robot.version.get_full_version())
    except ImportError:
        logger.critical("Robot Framework not installed in active Python interpreter")
        raise InjectionException("Robot Framework not installed")


def _get_connector(klass: str):
    try:
        module_name = klass.split(".")[:-1]
        cls_name = klass.split(".").pop()
        return getattr(import_module(".".join(module_name)), cls_name)  # get class from module
    except ImportError:
        err_msg = "Failed to inject %s class" % klass
        logger.critical(err_msg)
        raise InjectionException(err_msg)


def serve(config: ReactiveRobotModel):
    _check_robot_exists()

    loop = asyncio.get_event_loop()

    cls = _get_connector(config.connector.driver)
    connector = cls()
    connector.variable_parser = None
    coroutine = loop.run_in_executor(None, lambda: connector.bind(connection_url=config.connector.connection_url,
                                                                  bindings=config.bindings,
                                                                  **config.connector.args))

    logger.info(
        "%s Service Version %s has been started. Waiting for events." % (config.service_name, config.service_version))
    loop.run_until_complete(coroutine)

    loop.close()
