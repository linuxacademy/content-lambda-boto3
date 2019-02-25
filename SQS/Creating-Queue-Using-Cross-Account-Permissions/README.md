# Creating a Queue Using Cross-Account Permissions

SQS does not allow API calls such as [`CreateQueue`](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html) using [cross-account permissions](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-authentication-and-access-control.html#access-control). A workaround is to create and invoke a Lambda function in another account, in order to call that API.)

## Create AWS CLI profiles

Development account admin

```sh
aws configure --profile devadmin
```

Production account admin

```sh
aws configure --profile prodadmin
```

## Create Lambda function in production account

Function name: `CreateSQSQueue`

See [`lambda_function.py`](lambda_function.py) and assign role [`lambda_execution_role.json`](lambda_execution_role.json).

## Assign permissions to Lambda function

Add permissions to the production Lambda function allowing it to be invoked by the development account user:

```sh
aws lambda add-permission \
--function-name CreateSQSQueue \
--statement-id DevAccountAccess \
--action 'lambda:InvokeFunction' \
--principal 'arn:aws:iam::__DEVELOPMENT_ACCOUNT_NUMBER__:user/devadmin' \
--region us-east-2 \
--profile prodadmin
```

To view the policy:

```sh
aws lambda get-policy \
--function-name CreateSQSQueue \
--region us-east-2 \
--profile prodadmin
```

To remove the policy:

```sh
aws lambda remove-permission \
--function-name CreateSQSQueue \
--statement-id DevAccountAccess \
--region us-east-2 \
--profile prodadmin
```

## Invoke the production Lambda function from the development account

```sh
aws lambda invoke \
--function-name '__LAMBDA_FUNCTION_ARN__' \
--payload '{"QueueName": "MyQueue" }' \
--invocation-type RequestResponse \
--profile devadmin \
--region us-east-2 \
output.txt
```