import os

import boto3
from botocore.exceptions import ClientError

FLOWLOGS_GROUP_NAME = os.environ['FLOWLOGS_GROUP_NAME']
ROLE_ARN = os.environ['ROLE_ARN']

ec2 = boto3.client('ec2')
logs = boto3.client('logs')


def lambda_handler(event, context):

    try:
        # Extract the VPC ID from the event
        vpc_id = event['detail']['responseElements']['vpc']['vpcId']

        print('VPC: ' + vpc_id)

        try:
            response = logs.create_log_group(
                logGroupName=FLOWLOGS_GROUP_NAME)
        except ClientError:
            print(f"Log group '{FLOWLOGS_GROUP_NAME}' already exists.")

        # Get Flow Logs status
        response = ec2.describe_flow_logs(
            Filter=[
                {
                    'Name': 'resource-id',
                    'Values': [
                        vpc_id,
                    ]
                },
            ],
        )

        if len(response['FlowLogs']) > 0:
            print('VPC Flow Logs are ENABLED')
        else:
            print('VPC Flow Logs are DISABLED. Enabling...')

            response = ec2.create_flow_logs(
                ResourceIds=[vpc_id],
                ResourceType='VPC',
                TrafficType='ALL',
                LogGroupName=FLOWLOGS_GROUP_NAME,
                DeliverLogsPermissionArn=ROLE_ARN,
            )

            print('Created Flow Logs:' + response['FlowLogIds'][0])

    except Exception as e:
        print('Error - reason "%s"' % str(e))
