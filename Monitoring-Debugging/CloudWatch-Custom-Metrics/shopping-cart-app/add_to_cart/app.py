import json
import random

import boto3

cloudwatch = boto3.client('cloudwatch')


def lambda_handler(event, context):

    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'ItemsAddedToCart',
                'Value': random.randint(1, 20)
            },
        ],
        Namespace='ShoppingCartApp'
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            [
                {"itemID": "123456"},
                {"itemID": "234567"},
                {"itemID": "345678"}
            ]
        ),
    }
