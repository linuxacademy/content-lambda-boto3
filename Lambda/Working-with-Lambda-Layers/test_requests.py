# make an HTTP GET request to the provided URL and determine if the request was successful. If the request was successful, it prints 'Success!', and if an error occurred or the response was not valid, it prints 'An error has occurred.'.
# This code is intended to be used as an AWS Lambda function that can be triggered by an event or schedule. 

import requests


def lambda_handler(event, context):

    response = requests.get('https://linuxacademy.com')
    if response:
        print('Success!')
    else:
        print('An error has occurred.')
