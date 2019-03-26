import logging
import uuid

import boto3
import requests
from flask import Flask

from aws_xray_sdk.core import patch_all, xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Patch all supported modules to enable automatic instrumentation
patch_all()

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
table = dynamodb.Table('Flask')


@app.route('/')
def hello_world():
    r = requests.get("https://linuxacademy.com")

    logger.debug(r.text)

    xray_recorder.begin_subsegment('DynamoDB PutItem')
    table.put_item(
        Item={
            'key': str(uuid.uuid1()),
            'response': r.text
        }
    )
    xray_recorder.end_subsegment()

    return 'Hello, World: %s' % r.url


if __name__ == '__main__':
    app.run(debug=True)
