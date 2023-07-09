import boto3 #library used to create ec2_client object to interact with EC2 INSTANCES INSIDE OF AWS


def lambda_handler(event, context):

    # Get list of regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               # retrieves a list of available AWS regions by calling ec2_client.describe_regions(). The response is a dictionary containing information about the regions. The code extracts the region names and stores them inside of the regions list
               for region in ec2_client.describe_regions()['Regions']]

    # Iterate over each region
    for region in regions:
        #creates an EC2 resource object (ec2) for the current region using boto3.resource('ec2', region_name=region).
        ec2 = boto3.resource('ec2', region_name=region)
        #prints the current region to the console 
        print("Region:", region)

        #code filters the EC2 instances in the current region to get only the running instances. 
        #It uses ec2.instances.filter() and specifies a filter to include instances with the state 'running'
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name',
                      'Values': ['running']}])

        # Stop the instances
        for instance in instances:
            instance.stop()
            #prints the id of each stopped instance 
            print('Stopped instance: ', instance.id)
