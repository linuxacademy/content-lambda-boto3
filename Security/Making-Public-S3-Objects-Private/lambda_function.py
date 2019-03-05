import os

import boto3

s3 = boto3.client('s3')

BUCKET_NAME = os.environ['BUCKET_NAME']


def lambda_handler(event, context):
    """Lambda entry point"""
    # Get bucket name from the event
    bucket = event['detail']['requestParameters']['bucketName']
    if (bucket != BUCKET_NAME):
        print(f"Doing nothing for bucket {bucket}.")
        return

    # Get key name from the event
    key = event['detail']['requestParameters']['key']

    # If object is not private then make it private
    if not (is_private(bucket, key)):
        print(f"Object with key {key} in bucket {bucket} is not private!")
        make_private(bucket, key)
    else:
        print(f"Object with key {key} in bucket {bucket} is already private.")


def is_private(bucket, key):
    """Check if an S3 object is private"""
    # Get the object ACL from S3
    acl = s3.get_object_acl(Bucket=bucket, Key=key)

    # Private object should have only one grant which is the object owner
    if (len(acl['Grants']) > 1):
        return False

    # If owner and grantee ids do no match, then the object is not private
    owner_id = acl['Owner']['ID']
    grantee_id = acl['Grants'][0]['Grantee']['ID']
    if (owner_id != grantee_id):
        return False
    return True


def make_private(bucket, key):
    """Make an object private"""
    s3.put_object_acl(Bucket=bucket, Key=key, ACL="private")
    print(f"Object with key {key} in bucket {bucket} is marked as private.")
