import os


AWS_REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-west-2')
ENV_NAME = os.environ.get('AWS_PROFILE', 'dev')
STREAM_NAME = os.environ.get('STREAM_NAME', 'biz-pri-v2-data')
APP_NAME = os.environ.get('APP_NAME', 'example')
DEBUG = os.getenv("DEBUG", "False").lower() == "false"
