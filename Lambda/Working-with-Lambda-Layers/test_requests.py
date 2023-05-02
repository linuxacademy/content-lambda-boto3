import requests


def lambda_handler(event, context):

    response = requests.get('https://www.google.com') # in place of ('https://linuxacademy.com')
    if response:
        print('Success!')
    else:
        print('An error has occurred.')
