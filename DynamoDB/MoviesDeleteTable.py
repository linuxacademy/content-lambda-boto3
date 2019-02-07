import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Movies')

table.delete()
