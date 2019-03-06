from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

AWS_EMAIL_REGION = 'us-east-1'            # SES isn't available in all regions
EMAIL_FROM = 'linuxacademylab@gmail.com'  # Use a verified SES email address
EMAIL_TO = 'linuxacademylab@gmail.com'
MAX_AGE = 90

iam = boto3.client('iam')
ses = boto3.client('ses', region_name=AWS_EMAIL_REGION)


def lambda_handler(event, context):

    paginator = iam.get_paginator('list_users')

    for response in paginator.paginate():

        for user in response['Users']:
            username = user['UserName']
            res = iam.list_access_keys(UserName=username)

            for access_key in res['AccessKeyMetadata']:
                access_key_id = access_key['AccessKeyId']
                create_date = access_key['CreateDate']
                print(f'User: {username} {access_key_id} {create_date}')
                age = days_old(create_date)
                if age < MAX_AGE:
                    continue

                # Expire the key
                print(f'Key {access_key_id} for user {username} is expired '
                      f'(age={age} days).')

                iam.update_access_key(
                    UserName=username,
                    AccessKeyId=access_key_id,
                    Status='Inactive')

                send_email_report(EMAIL_TO, username, age, access_key_id)


def days_old(create_date):
    now = datetime.now(timezone.utc)
    age = now - create_date
    return age.days


def send_email_report(email_to, username, age, access_key_id):
    data = (f'Access Key {access_key_id} belonging to user {username} has been '
            f'automatically deactivated due to it being {age} days old.')

    try:
        response = ses.send_email(
            Source=EMAIL_FROM,
            Destination={
                'ToAddresses': [EMAIL_TO]
            },
            Message={
                'Subject': {
                    'Data': ('AWS IAM Access Key Rotation - Deactivation of '
                             f'Access Keys: {access_key_id}')
                },
                'Body': {
                    'Text': {
                        'Data': data
                    }
                }
            })
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:" + response['MessageId'])
