import os

import boto3

TABLE_NAME = os.environ['TABLE_NAME']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
s3 = boto3.resource('s3')
rekognition = boto3.client('rekognition')


def lambda_handler(event, context):

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    obj = s3.Object(bucket, key)
    image = obj.get()['Body'].read()
    print('Recognizing celebrities...')
    response = rekognition.recognize_celebrities(Image={'Bytes': image})

    names = []

    for celebrity in response['CelebrityFaces']:
        name = celebrity['Name']
        print('Name: ' + name)
        names.append(name)

    print(names)

    print('Saving face data to DynamoDB table:', TABLE_NAME)
    response = table.put_item(
        Item={
            'key': key,
            'names': names,
        }
    )
    print(response)
