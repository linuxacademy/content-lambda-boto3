import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import boto3

ssm = boto3.client('ssm')


def lambda_handler(event, context):
    print(json.dumps(event))

    message = json.loads(event['Records'][0]['Sns']['Message'])
    print(json.dumps(message))

    alarm_name = message['AlarmName']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']

    slack_message = {
        'text': f':fire: {alarm_name} state is now {new_state}: {reason}\n'
                f'```\n{message}```'
    }

    webhook_url = ssm.get_parameter(
        Name='SlackWebHookURL', WithDecryption=True)

    req = Request(webhook_url['Parameter']['Value'],
                  json.dumps(slack_message).encode('utf-8'))

    try:
        response = urlopen(req)
        response.read()
        print(f"Message posted to Slack")
    except HTTPError as e:
        print(f'Request failed: {e.code} {e.reason}')
    except URLError as e:
        print(f'Server connection failed: {e.reason}')
