from datetime import datetime
import json
import os
import boto3

DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Count items in the Lambda event 
    no_messages = str(len(event['Records']))
    print("Found " +no_messages +" messages to process.")

    for message in event['Records']:

        print(message)

        # Write message to DynamoDB
        table = dynamodb.Table(DYNAMODB_TABLE)

        response = table.put_item(
            Item={
                'MessageId': message['messageId'],
                'Body': message['body'],
                'Timestamp': datetime.now().isoformat()
            }
        )
        print("Wrote message to DynamoDB:", json.dumps(response))
