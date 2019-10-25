import datetime

from marshmallow import Schema, fields


class DateTimeCompat(fields.DateTime):
    """
    This class supports serialization / deserialization using ISO date/time format, with the Z UTC identifier
    instead of the ISO format of +00:00 UTC identifier for compatility with java (legacy system)
    """
    def _serialize(self, value, attr, obj, **kwargs):
        return super()._serialize(value, attr, obj, **kwargs).replace('+00:00', 'Z')

    def _deserialize(self, value, attr, data, **kwargs):
        return super()._deserialize(value.replace('Z', '+00:00'), attr, data, **kwargs)


class ApiInfo(Schema):
    date = DateTimeCompat(data_key="date")
    api_version = fields.Str(data_key="apiVersion")
    api_name = fields.Str(data_key="apiName")


class Echo(Schema):
    date = DateTimeCompat(data_key="date", dump_only=True, default=datetime.datetime.now())
    message = fields.Str(data_key="message")
