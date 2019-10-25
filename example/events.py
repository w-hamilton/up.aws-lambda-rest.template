import datetime
import json

import uuid
import boto3

from botocore.exceptions import ClientError
from example.exceptions import UpException
from example import settings

KINESIS_INSTANCE = None  # Lazy init kinesis


def get_kinesis_instance():
    global KINESIS_INSTANCE
    if KINESIS_INSTANCE is None:
        KINESIS_INSTANCE = boto3.client('kinesis', region_name=settings.AWS_REGION)
    return KINESIS_INSTANCE


def get_request_id(context: (dict, object, None)) -> str:
    if context and 'aws_request_id' in context:
        return context.aws_request_id
    if 'requestId' in context:
        return context['requestId']
    else:
        return str(uuid.uuid4())


def record_event(payload: dict, **kwargs) -> bool:
    kinesis = get_kinesis_instance()
    event = {
        "rtype": settings.APP_NAME,
        "env": settings.ENV_NAME,
        "timestamp": datetime.datetime.utcnow().isoformat() + 'Z',
        "payload": payload
    }
    merged = {**event, **kwargs}
    event = json.dumps(merged) + '\n'
    try:
        #  TODO uncomment to enable Kinesis
        #  kinesis.put_record(StreamName=STREAM_NAME, Data=event, PartitionKey="default")
        print("kinesis.put_record(StreamName={}, Data={}, PartitionKey={})", settings.STREAM_NAME, event, "default", kinesis)
    except ClientError as e:
        print(e)
        return False
    return True


def record_payload(context: (dict, object, None), **kwargs) -> bool:
    context = {
        'resourcePath': None,
        'httpMethod': None,
        **context
    }
    payload = {
        "correlation-id": get_request_id(context),
        "communication-purpose": "{}-response".format(settings.APP_NAME),
        "resourcePath": context['resourcePath'],
        "httpMethod": context['httpMethod']
    }
    return record_event({**payload, **kwargs})


def record_exception(context: (dict, object, None), e: UpException, **kwargs) -> bool:
    payload = {
        "correlation-id": str(uuid.uuid4()),
        "communication-purpose": "{}-err-response".format(settings.APP_NAME)
    }
    return record_payload(context, **payload, error_msg=str(e.message), status_code=e.status_code, **kwargs)
