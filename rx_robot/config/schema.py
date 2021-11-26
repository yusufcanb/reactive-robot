from marshmallow import Schema, fields, post_load


class ConnectorSchema(Schema):
    driver = fields.String()
    credentials = fields.Date()


class RxRobotConfigSchema(Schema):
    service_name = fields.String(required=True)
    service_version = fields.String()

    connector = fields.Nested(ConnectorSchema(), allow_none=True)

    @post_load
    def post_validation(self, data, **kwargs):
        return data
