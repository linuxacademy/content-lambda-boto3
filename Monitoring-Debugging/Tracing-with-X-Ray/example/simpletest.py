import requests

response = requests.get('https://httpbin.org/ip')
print('requests Python library was loaded! check whether you can see the following ID report:')
print('Your IP is {0}'.format(response.json()['origin']))
