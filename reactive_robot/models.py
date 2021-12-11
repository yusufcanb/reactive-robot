import logging
from abc import ABC
from typing import List
from urllib.parse import urlparse

from reactive_robot.parsers.string import RawPayloadParser

logger = logging.getLogger("reactive_robot.models")


class Model(ABC):

    def __init__(self, *args, **kwargs):
        pass


class RobotModel(Model):
    file: str
    args: str

    def __init__(self, *args, **kwargs):
        self.file = kwargs.pop("file")
        self.args = kwargs.pop("args")
        super(RobotModel, self).__init__(*args, **kwargs)


class ConnectorModel(Model):
    driver: str
    connection_url: str
    args: dict
    variable_parser = RawPayloadParser()

    def __init__(self, *args, **kwargs):
        self.driver = kwargs.pop("driver")
        self.connection_url = urlparse(kwargs.pop("connection_url"))
        self.args = kwargs.pop("args", {})
        super(ConnectorModel, self).__init__(*args, **kwargs)


class BindingModel(Model):
    name: str
    topic: str
    robot: RobotModel

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop("name")
        self.topic = kwargs.pop("topic")
        self.robot = RobotModel(**kwargs.pop("robot", {}))
        super(BindingModel, self).__init__(*args, **kwargs)


class ReactiveRobotModel(Model):
    service_name: str = "Reactive Robot Service"
    service_version: str = "0.1.0"

    connector: ConnectorModel = None
    bindings: List[BindingModel] = []

    def set_connector(self, connector: ConnectorModel):
        self.connector = connector

    def add_binding(self, binding: BindingModel):
        self.bindings.append(binding)

    @classmethod
    def from_dict(cls, **kwargs):
        model = ReactiveRobotModel()

        model.service_name = kwargs.pop("service_name")
        model.service_version = kwargs.pop("service_version")

        model.connector = ConnectorModel(**kwargs.pop("connector"))

        bindings = kwargs.pop("bindings", [])
        model.bindings = [BindingModel(**bd) for bd in bindings]

        logger.debug("Using configuration model, %s" % model)
        return model

    def __str__(self):
        return "<ReactiveRobotModel %s-%s>" % (self.service_name, self.service_version)
