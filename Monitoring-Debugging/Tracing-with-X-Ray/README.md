# Tracing with X-Ray

## Create DynamoDB Table

Create table `Flask` with primary partition key `key`:

```sh
aws dynamodb create-table --table-name Flask \
  --attribute-definitions AttributeName=key,AttributeType=S \
  --key-schema AttributeName=key,KeyType=HASH \
  --billing-mode=PAY_PER_REQUEST
```

## Configure [Zappa](https://github.com/Miserlou/Zappa)

```sh
cd example
pipenv --python 3.7
pipenv shell
pipenv install aws-xray-sdk flask zappa requests
pipenv lock -r > requirements.txt
zappa init
```

Add the following property to `zappa_settings.json`:

```json
"xray_tracing": true
```

Deploy the application:

```sh
zappa deploy
```

## Enable X-Ray Tracing for API Gateway

In this step you will interact with the API Gateway console to enable X\-Ray tracing\.

1. Sign in to the AWS Management Console and open the API Gateway console at <https://console\.aws\.amazon\.com/apigateway/>.
1. Select your API, i.e. `example-dev`.
1. Choose **Stages**.
1. Choose the name of your deployment stage, i.e. `dev`.
1. On the **Logs/Tracing** tab, select the **Enable X-Ray Tracing** box.
1. Choose **Save Changes**.
1. Access the endpoint in your browser.
