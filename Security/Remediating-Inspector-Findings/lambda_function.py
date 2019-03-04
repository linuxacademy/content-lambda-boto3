import json

import boto3

ssm = boto3.client('ssm')
inspector = boto3.client('inspector')


def lambda_handler(event, context):

    print(json.dumps(event))

    # extract the message that Inspector sent via SNS
    message = event['Records'][0]['Sns']['Message']

    # get inspector notification type
    notificationType = json.loads(message)['event']
    print('Inspector SNS message type: ' + notificationType)

    # skip everything except report_finding notifications
    if notificationType != "FINDING_REPORTED":
        print('Skipping notification that is not a new finding: ' +
              notificationType)
        return 1

    # extract finding ARN
    findingArn = json.loads(message)['finding']
    print('Finding ARN: ' + findingArn)

    # get finding and extract detail
    response = inspector.describe_findings(
        findingArns=[findingArn], locale='EN_US')

    finding = response['findings'][0]

    # skip uninteresting findings
    title = finding['title']

    if title == "Unsupported Operating System or Version":
        print('Skipping finding: ' + title)
        return 1

    if title == "No potential security issues found":
        print('Skipping finding: ' + title)
        return 1

    service = finding['service']

    if service != "Inspector":
        print('Skipping finding from service: ' + service)
        return 1

    cveId = ""
    for attribute in finding['attributes']:
        if attribute['key'] == "CVE_ID":
            cveId = attribute['value']
            break
    print('CVE ID: ' + cveId)

    if cveId == "":
        print('Skipping non-CVE finding (could not find CVE ID)')
        return 1

    assetType = finding['assetType']

    if assetType != "ec2-instance":
        print('Skipping non-EC2-instance asset type: ' + assetType)
        return 1

    instanceId = finding['assetAttributes']['agentId']
    print('Instance ID: ' + instanceId)
    if not instanceId.startswith("i-"):
        print('Invalid instance ID: ' + instanceId)
        return 1

    # if we got here, we have a valid CVE type finding for an EC2 instance
    # with a well-formed instance ID

    # query SSM for information about this instance
    filterList = [{'key': 'InstanceIds', 'valueSet': [instanceId]}]
    response = ssm.describe_instance_information(
        InstanceInformationFilterList=filterList, MaxResults=50)

    instanceInfo = response['InstanceInformationList'][0]

    pingStatus = instanceInfo['PingStatus']
    print('SSM status of instance: ' + pingStatus)

    platformType = instanceInfo['PlatformType']
    print('OS type: ' + platformType)

    osName = instanceInfo['PlatformName']
    print('OS name: ' + osName)

    osVersion = instanceInfo['PlatformVersion']
    print('OS version: ' + osVersion)

    # Terminate if SSM agent is offline
    if pingStatus != 'Online':
        print('SSM agent for this instance is not online: ' + pingStatus)
        return 1

    # This script only supports remediation on Linux
    if platformType != "Linux":
        print('Skipping non-Linux platform: ' + platformType)
        return 1

    # Look up the correct command to update this Linux distro
    if osName.startswith('Ubuntu'):
        commandLine = "apt-get update -qq -y; apt-get upgrade -y"
    elif osName.startswith('Amazon Linux'):
        commandLine = "yum update -q -y; yum upgrade -y"
    else:
        print('Unsupported Linux distribution: ' + osName)
        return 1
    print('Command line to execute: ' + commandLine)

    # Run command using SSM
    response = ssm.send_command(
        InstanceIds=[instanceId],
        DocumentName='AWS-RunShellScript',
        Comment='Lambda performing Inspector CVE finding auto-remediation',
        Parameters={'commands': [commandLine]}
    )

    print('SSM send-command response:')
    print(response)
