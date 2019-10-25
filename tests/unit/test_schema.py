import datetime

from marshmallow import ValidationError

from example import models, settings


def test_example_schema_data():
    try:
        response_schema = models.ApiInfo()
        response = response_schema.dump(dict(date=datetime.datetime.now(), api_version=1, api_name=settings.APP_NAME))
        print(response)
    except ValidationError as err:
        print(err.messages)  # => {"email": ['"foo" is not a valid email address.']}
        print(err.valid_data)  # => {"name": "John"}
