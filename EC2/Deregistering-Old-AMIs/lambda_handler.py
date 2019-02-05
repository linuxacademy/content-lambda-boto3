import datetime
from dateutil.parser import parse

import boto3


def days_old(date):
    parsed = parse(date).replace(tzinfo=None)
    diff = datetime.datetime.now() - parsed
    return diff.days


def lambda_handler(event, context):

    # Get list of regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]

    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        print("Region:", region)

        amis = ec2.describe_images(Owners=['self'])['Images']

        for ami in amis:
            creation_date = ami['CreationDate']
            age_days = days_old(creation_date)
            image_id = ami['ImageId']
            print('ImageId: {}, CreationDate: {} ({} days old)'.format(
                image_id, creation_date, age_days))

            if age_days >= 2:
                print('Deleting ImageId:', image_id)

                # Deregister the AMI
                ec2.deregister_image(ImageId=image_id)
