import json

import boto3

ec2 = boto3.client('ec2')


def lambda_handler(event, context):
    sns = event['Records'][0]['Sns']
    json_msg = json.loads(sns['Message'])

    # Extract the EC2 instance ID
    instance = json_msg['AlarmDescription'].split()[-1]

    ec2.stop_instances(InstanceIds=[instance])

    print('Stopped instance: %s' % instance)
