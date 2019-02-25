import boto3

sqs = boto3.resource('sqs')


def lambda_handler(event, context):

    queue = sqs.create_queue(QueueName=event['QueueName'])
    print('Queue URL', queue.url)
