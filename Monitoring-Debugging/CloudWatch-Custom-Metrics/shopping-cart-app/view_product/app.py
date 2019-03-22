import json

import boto3

cloudwatch = boto3.client('cloudwatch')


def lambda_handler(event, context):

    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'ViewProduct',
                'Value': 1
            },
        ],
        Namespace='ShoppingCartApp'
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "ProductID": "123456",
        }),
    }
