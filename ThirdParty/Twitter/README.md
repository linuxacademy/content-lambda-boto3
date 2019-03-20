# Creating a Twitter App

In this lesson, you will learn to create a Twitter app that automatically sends tweets on a schedule.

## Create Twitter Application

More info here <https://developer.twitter.com/en/docs/basics/apps/overview>.

Note the Consumer API keys and Access token & access token secret.

```sh
CONSUMER_KEY=...
CONSUMER_SECRET=...
ACCESS_TOKEN=...
ACCESS_TOKEN_SECRET=...
```

## Create SSM Parameters

Use the keys from the previous step:

```sh
aws ssm put-parameter --cli-input-json '{"Type": "SecureString", "KeyId": "alias/aws/ssm", "Name": "/TwitterBot/consumer_key", "Value": "'"$CONSUMER_KEY"'"}'

aws ssm put-parameter --cli-input-json '{"Type": "SecureString", "KeyId": "alias/aws/ssm", "Name": "/TwitterBot/consumer_secret", "Value": "'"$CONSUMER_SECRET"'"}'

aws ssm put-parameter --cli-input-json '{"Type": "SecureString", "KeyId": "alias/aws/ssm", "Name": "/TwitterBot/access_token", "Value": "'"$ACCESS_TOKEN"'"}'

aws ssm put-parameter --cli-input-json '{"Type": "SecureString", "KeyId": "alias/aws/ssm", "Name": "/TwitterBot/access_token_secret", "Value": "'"$ACCESS_TOKEN_SECRET"'"}'
```

## Create an S3 bucket and upload the data file

```sh
aws s3 mb s3://123456789012-twitterbot
aws s3 cp data.txt s3://123456789012-twitterbot
```

## Create IAM execution role for Lambda

Grant access to your S3 bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "s3:GetObject"
    ],
    "Resource": "arn:aws:s3:::123456789012-twitterbot/*"
  }]
}
```

## Create deployment package

Create a new virtual environment using `pipenv` and install the required libraries:

```sh
pipenv --python 3.7
pipenv shell
pipenv install tweepy
mkdir package
pipenv lock -r > requirements.txt
pip install -r requirements.txt --no-deps -t package
cd package
zip -r9 ../package.zip .
cd ..
zip -g package.zip lambda_handler.py
rm -rf package/*
```

<!--
## Update Lambda funcion

```sh
aws lambda update-function-code --function-name TwitterBot --zip-file fileb://package.zip
``` -->

## Create Lambda function

```sh
aws lambda create-function \
--function-name TwitterBot \
--zip-file fileb://package.zip \
--role arn:aws:iam::123456789012:role/LambdaTwitterBotRole \
--handler lambda_function.lambda_handler \
--runtime python3.7 \
--environment Variables={BUCKET_NAME=123456789012-twitterbot}
```

## Create CloudWatch Scheduled Rule

```sh
aws events put-rule \
--name TwitterBot \
--schedule-expression 'rate(1 hour)'

aws lambda add-permission \
--function-name TwitterBot \
--statement-id TwitterBot \
--action 'lambda:InvokeFunction' \
--principal events.amazonaws.com \
--source-arn arn:aws:events:us-east-1:123456789012:rule/TwitterBot

aws events put-targets --rule TwitterBot --targets file://targets.json
```