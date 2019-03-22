import json
import decimal
import random

import boto3

cloudwatch = boto3.client('cloudwatch')


def lambda_handler(event, context):

    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'OrderTotal',
                'Value': decimal.Decimal(random.randrange(100, 50000))/100
            },
        ],
        Namespace='ShoppingCartApp'
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "OrderID": "123456",
            "OrderTotal": "543.21",
        }),
    }
