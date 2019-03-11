import json
import os
import uuid
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

CHARSET = 'UTF-8'
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
SENDER_EMAIL = os.environ['SENDER_EMAIL']  # Must be configured in SES
SES_REGION = 'us-east-1'


dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name=SES_REGION)


def lambda_handler(event, context):
    print(event)
    data = json.loads(event['body'])
    print(json.dumps(data))

    try:

        content = 'Message from ' + \
            data['first_name'] + ' ' + data['last_name'] + '\n' + \
            data['company'] + '\n' + \
            data['address1'] + '\n' + \
            data['address2'] + '\n' + \
            data['city'] + '\n' + \
            data['state'] + '\n' + \
            data['zip'] + '\n' + \
            data['email'] + '\n' + \
            data['phone'] + '\n' + \
            data['budget'] + '\n' + \
            data['message']
        save_to_dynamodb(data)
        response = send_mail_to_user(data, content)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message Id:", response['MessageId'])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": ""
    }


def save_to_dynamodb(data):
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
    table = dynamodb.Table(DYNAMODB_TABLE)
    item = {
        'id': str(uuid.uuid1()),
        'first_name': data['first_name'],  # required
        'last_name': data['last_name'],  # required
        'company': data['company'] if data['company'] else None,
        'address1': data['address1'] if data['address1'] else None,
        'address2': data['address2'] if data['address2'] else None,
        'city': data['city'] if data['city'] else None,
        'state': data['state'] if data['state'] else None,
        'zip': data['zip'] if data['zip'] else None,
        'email': data['email'],  # required
        'phone': data['phone'],  # required
        'budget': data['budget'],  # required
        'message': data['message'],  # required
        'createdAt': timestamp,
        'updatedAt': timestamp
    }
    table.put_item(Item=item)
    return


def send_mail_to_user(data, content):
    return ses.send_email(
        Source=SENDER_EMAIL,
        Destination={
            'ToAddresses': [
                data['email'],
            ],
        },
        Message={
            'Subject': {
                'Charset': CHARSET,
                'Data': 'Thank you for contacting us!'
            },
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': content
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': content
                }
            }
        }
    )
