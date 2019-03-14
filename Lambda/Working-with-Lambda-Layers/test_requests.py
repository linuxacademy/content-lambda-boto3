import requests


def lambda_handler(event, context):

    response = requests.get('https://linuxacademy.com')
    if response:
        print('Success!')
    else:
        print('An error has occurred.')
