import boto3
import json

config = boto3.client('config')


def lambda_handler(event, context):
    invoking_event = json.loads(event['invokingEvent'])
    rule_parameters = json.loads(event['ruleParameters'])

    compliance_value = 'NOT_APPLICABLE'

    if is_applicable(invoking_event['configurationItem'], event):
        compliance_value = evaluate_compliance(
            invoking_event['configurationItem'], rule_parameters)

    response = config.put_evaluations(
        Evaluations=[
            {
                'ComplianceResourceType': invoking_event['configurationItem']['resourceType'],
                'ComplianceResourceId': invoking_event['configurationItem']['resourceId'],
                'ComplianceType': compliance_value,
                'OrderingTimestamp': invoking_event['configurationItem']['configurationItemCaptureTime']
            },
        ],
        ResultToken=event['resultToken'])


def is_applicable(config_item, event):
    status = config_item['configurationItemStatus']
    event_left_scope = event['eventLeftScope']
    test = ((status in ['OK', 'ResourceDiscovered']) and
            event_left_scope == False)
    return test


def evaluate_compliance(config_item, rule_parameters):
    if (config_item['resourceType'] != 'AWS::EC2::Instance'):
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
