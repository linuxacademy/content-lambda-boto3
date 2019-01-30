from datetime import datetime

import boto3


def lambda_handler(event, context):

    account_id = boto3.client('sts').get_caller_identity().get('Account')
    ec2 = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2.describe_regions()['Regions']]

    for region in regions:
        print("Region:", region)
        ec2 = boto3.client('ec2', region_name=region)
        snapshots = ec2.describe_snapshots(OwnerIds=[account_id])

        for snapshot in snapshots['Snapshots']:
            print("Found snapshot:", snapshot)
            start_time = snapshot['StartTime'].date()
            today = datetime.utcnow().date()
            age = today - start_time
            try:
                if age.days > 30:
                    id = snapshot['SnapshotId']
                    print("Deleting snapshot:", id)
                    ec2.delete_snapshot(SnapshotId=id)
            except Exception as e:
                if 'InvalidSnapshot.InUse' in e.message:
                    print("Snapshot {} in use, skipping.".format(id))
                    continue
