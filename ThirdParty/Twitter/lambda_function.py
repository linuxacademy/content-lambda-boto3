import os
import random

import boto3
from botocore.exceptions import ClientError
import tweepy

BUCKET_NAME = os.environ['BUCKET_NAME']
KEY = 'data.txt'

s3 = boto3.resource('s3')
ssm = boto3.client('ssm')


def get_parameter(param_name):
    response = ssm.get_parameter(Name=param_name, WithDecryption=True)
    credentials = response['Parameter']['Value']
    return credentials


def get_tweet_text():
    filename = '/tmp/' + KEY
    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, filename)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f'The object {KEY} does not exist in bucket {BUCKET_NAME}.')
        else:
            raise

    with open(filename) as f:
        lines = f.readlines()
        return random.choice(lines)


def lambda_handler(event, context):

    # Get SSM parameters
    CONSUMER_KEY = get_parameter('/TwitterBot/consumer_key')
    CONSUMER_SECRET = get_parameter('/TwitterBot/consumer_secret')
    ACCESS_TOKEN = get_parameter('/TwitterBot/access_token')
    ACCESS_TOKEN_SECRET = get_parameter('/TwitterBot/access_token_secret')

    # Authenticate Tweepy
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Send tweet
    tweet = get_tweet_text()
    print(tweet)
    api.update_status(tweet)
