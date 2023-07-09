
#this code is likely part of an AWS Lambda function that listens for S3 events (such as object uploads) and uses the Rekognition service to recognize celebrities in the uploaded images. 
#It then stores the extracted face data (key and names) in a DynamoDB table.

import os
import boto3

#enviornment variable that is set outside of this code
TABLE_NAME = os.environ['TABLE_NAME']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
s3 = boto3.resource('s3')
rekognition = boto3.client('rekognition')

#extracts information about an s3 object that triggered the lambda functino by passing in the even parameter. This is an entrypoint for the Lambda function when the Lambda function is triggered.
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
    #put_item is a method from the table object 
    print('Saving face data to DynamoDB table:', TABLE_NAME)
    response = table.put_item(
        Item={
            'key': key,
            'names': names,
        }
    )
    print(response)
