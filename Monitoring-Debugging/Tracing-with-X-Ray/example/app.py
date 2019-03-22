import json
import logging
import uuid

import boto3
import requests
from flask import Flask

from aws_xray_sdk.core import patcher, xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Patch the requests module to enable automatic instrumentation
patcher.patch(('requests',))

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Configure the X-Ray recorder to generate segments with our service name
xray_recorder.configure(service='Example Flask App')

# Instrument the Flask application
XRayMiddleware(app, xray_recorder)

# Boto3 resources
dynamodb = boto3.resource('dynamodb')
ssm = boto3.client('ssm')

table_param = ssm.get_parameter(Name='/dev/example/table_name')
table_name = table_param['Parameter']['Value']

logger.info('Table name:' + table_name)

table = dynamodb.Table(table_name)


@app.route('/')
def hello_world():
    r = requests.get("https://linuxacademy.com")

    logger.debug(r.text)

    table.put_item(
        Item={
            'key': str(uuid.uuid1()),
            'response': r.text
        }
    )

    return 'Hello, World: %s' % r.url


if __name__ == '__main__':
    app.run(debug=True)
