import json

from chalice.config import Config
from chalice.local import LocalGateway
from example.controller import app

HEADERS = {
    'Content-Type': 'application/json'
}


def call_api(method: str, path: str, headers: (dict, None) = None, body: str = ""):
    gateway = LocalGateway(app, Config())
    headers = HEADERS if headers is None else {**HEADERS, **headers}
    return gateway.handle_request(method=method, path=path, headers=headers, body=body)


def test_api_info():
    response = call_api(method='GET', path='/example/v1/info')
    assert response['statusCode'] == 200


def test_echo():
    response = call_api(method='POST', path='/example/v1/echo', body=open('tests/resources/echo_data.json').read())
    assert response['statusCode'] == 200
    parsed_response = json.loads(response['body'])
    assert parsed_response['message'] == 'Hello World!'

