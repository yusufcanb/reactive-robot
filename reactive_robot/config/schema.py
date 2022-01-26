from marshmallow import Schema, fields, post_load

from reactive_robot.models import ReactiveRobotModel


class ConnectorSchema(Schema):
    driver = fields.String()
    connection_url = fields.String()
    args = fields.Dict()


class RobotSchema(Schema):
    file = fields.Field()
    args = fields.String(allow_none=True)


class BindingSchema(Schema):
    name = fields.String()
    topic = fields.String()
    robot = fields.Nested(RobotSchema(), allow_none=True)


class S3Schema(Schema):
    host = fields.Url()
    bucket_name = fields.String()
    access_key = fields.String()
    access_secret = fields.String()


class RxRobotConfigSchema(Schema):
    service_name = fields.String(required=True)
    service_version = fields.String()

    connector = fields.Nested(ConnectorSchema(), allow_none=True)
    bindings = fields.List(fields.Nested(BindingSchema()))

    @post_load
    def post_validation(self, data, **kwargs):
        return ReactiveRobotModel.from_dict(**data)
