import datetime
import json

import yaml
from chalice.app import Request
from marshmallow import ValidationError

from example import models, settings, events
import chalice

from typing import Callable, Optional, List
from chalice import Response
from example.exceptions import UpException

app = chalice.Chalice(app_name=settings.APP_NAME)
app.debug = settings.DEBUG

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
    "Access-Control-Max-Age": "600"
}


def validate_route(input_schema: Optional[Callable] = None) -> Callable:
    """Decorator to handle exceptions and optionally validate input marshmallow.Schema"""
    def decorator_fn(route_fn: Callable) -> Callable:
        def decorator() -> Response:
            try:
                if input_schema is not None:
                    try:
                        return route_fn(input_schema().load(app.current_request.json_body))
                    except ValidationError as err:
                        return Response(body={"error": err.messages}, headers=headers, status_code=400)
                return route_fn()
            except UpException as e:  # Generic uncaught specialized exception
                events.record_exception(app.current_request.context, e)
                return Response(body={"error": str(e.message)}, headers=headers, status_code=e.status_code)
        return decorator
    return decorator_fn


@app.route("/example/v1/info", methods=["GET"])
@validate_route()
def api_info():
    response_schema = models.ApiInfo()
    response = json.dumps(response_schema.dump(dict(
        date=datetime.datetime.now(), api_version=1, api_name=settings.APP_NAME
    )))

    # Write the Response to Kinesis?
    events.record_event(response)

    # Return response for the consumer
    return Response(body=response, headers=headers, status_code=200)


@app.route("/example/v1/echo", methods=["POST"])
@validate_route(input_schema=models.Echo)
def api_info(validated_body):
    response_schema = models.Echo()
    response = json.dumps(response_schema.dump(validated_body))

    # Write the Response to Kinesis?
    events.record_event(response)

    # Return response for the consumer
    return Response(body=response, headers=headers, status_code=200)
