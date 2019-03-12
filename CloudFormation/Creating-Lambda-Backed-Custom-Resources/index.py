import json

import cfnresponse


def lambda_handler(event, context):
    print(json.dumps(event))
    response_data = {}
    response_data['Data'] = None

    if event['RequestType'] != 'Create':
        cfnresponse.send(event, context, cfnresponse.SUCCESS,
                         response_data, "CustomResourcePhysicalID")
        return

    password = event['ResourceProperties']['Password']
    confirm_password = event['ResourceProperties']['ConfirmPassword']

    if password == confirm_password:
        cfnresponse.send(event, context, cfnresponse.SUCCESS,
                         response_data, "CustomResourcePhysicalID")
    else:
        print('Passwords do not match!')
        cfnresponse.send(event, context, cfnresponse.FAILED,
                         response_data, "CustomResourcePhysicalID")
