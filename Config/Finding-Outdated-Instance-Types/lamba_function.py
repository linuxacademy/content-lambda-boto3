import json

import boto3

config = boto3.client('config')


def lambda_handler(event, context):
    invoking_event = json.loads(event['invokingEvent'])
    rule_parameters = json.loads(event['ruleParameters'])  # i.e. 't2.micro'

    compliance_value = 'NOT_APPLICABLE'
    item = invoking_event['configurationItem']  # one per AWS resource

    if is_applicable(item, event):
        compliance_value = evaluate_compliance(item, rule_parameters)

    config.put_evaluations(
        Evaluations=[
            {
                'ComplianceResourceType': item['resourceType'],
                'ComplianceResourceId': item['resourceId'],
                'ComplianceType': compliance_value,
                'OrderingTimestamp': item['configurationItemCaptureTime']
            },
        ],
        ResultToken=event['resultToken'])


def is_applicable(item, event):
    status = item['configurationItemStatus']
    event_left_scope = event['eventLeftScope']
    test = ((status in ['OK', 'ResourceDiscovered']) and
            event_left_scope is False)
    return test


def evaluate_compliance(config_item, rule_parameters):
    if config_item['resourceType'] != 'AWS::EC2::Instance':
        return 'NOT_APPLICABLE'

    instance_id = config_item['configuration']['instanceId']
    instance_type = config_item['configuration']['instanceType']

    print(f"Instance {instance_id} {instance_type} is ", end='')

    if (config_item['configuration']['instanceType'] in
            rule_parameters['desiredInstanceType']):
        print('COMPLIANT')
        return 'COMPLIANT'
    else:
        print('NON_COMPLIANT')
        return 'NON_COMPLIANT'
