# Creating a Queue Using Cross-Account Roles

SQS does not allow API calls such as [`CreateQueue`](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html) using [cross-account permissions](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-authentication-and-access-control.html#access-control). A workaround is to create and invoke a Lambda function in another account, in order to call that API.

## Create AWS CLI profiles

Production Admin (trusting account)

```sh
aws configure --profile prodadmin
```

Development Admin (trusted account)

```sh
aws configure --profile devadmin
```

Development User (trusted account)

```sh
aws configure --profile devuser
```

## Create a role in the trusting ("prod") account

Role name: `CreateSQSQueueRole`

**`create-queue-policy.json`**

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sqs:CreateQueue",
            "Resource": "*"
        }
    ]
}
```

**`trust-policy-for-dev.json`**


```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal":
      {
        "AWS": "arn:aws:iam::__TRUSTED_ACCOUNT_NUMBER__:root"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### Create the role with the trust policy

The trust relationship policy document grants the **trusted** account permission to assume the role in the **trusting** account.

```sh
aws iam create-role --role-name CreateSQSQueueRole --assume-role-policy-document trust-policy-for-dev.json --profile prodadmin
```

**Note the Role ARN.**

### Attach the user policy

```sh
aws iam put-role-policy --role-name CreateSQSQueueRole --policy-name CreateSQSQueuePolicy --policy-document file://create-queue-policy.json --profile prodadmin
```

### List role policies

```sh
aws iam list-role-policies --role-name CreateSQSQueueRole --profile prodadmin
```

## Grant permissions to assume the role in the trusted account

The administrator of the **trusted** account must give specific groups or users in that account permission to switch to the role.

To grant a user permission to switch to a role, you create a new policy for the user or edit an existing policy to add the required elements.

**`devuser-policy.json`**

```json
{
  "Version": "2012-10-17",
  "Statement": {
    "Effect": "Allow",
    "Action": "sts:AssumeRole",
    "Resource": "arn:aws:iam::__TRUSTING_ACCOUNT_NUMBER__:role/CreateSQSQueueRole"
  }
}
```

```sh
aws iam create-policy --policy-name devuser-policy --policy-document file://devuser-policy.json --profile prodadmin
```

**Note the Role ARN.**

### Attach the policy to the user

Run as the administrator of the the **trusted** ("dev") account:

```sh
aws iam attach-user-policy --user-name devuser --policy-arn "arn:aws:iam::__TRUSTING_ACCOUNT_NUMBER__:policy/devuser-policy" --profile devadmin

aws iam list-attached-user-policies --user-name devuser --profile devadmin
```

## Assume the role from the trusted ("dev") account

Edit `~/.aws/config`, adding this **cross-account** profile:

```ini
[profile crossaccount]
role_arn = arn:aws:iam::__TRUSTING_ACCOUNT_NUMBER__:role/CreateSQSQueueRole
source_profile = devuser
```

## Try creating an SQS queue as the assumed cross-account role

`aws sqs create-queue --queue-name MyQueue --profile crossaccount`

Fail.

## Create the Lambda function in the trusting ("prod") account

Function name: `CreateSQSQueue`

See [`lambda_function.py`](lambda_function.py) and assign role [`lambda_execution_role.json`](lambda_execution_role.json).

## Invoke the Lambda function, assuming the cross-account role from the trusted account

```sh
aws lambda invoke --function-name arn:aws:lambda:us-east-1:__TRUSTING_ACCOUNT_NUMBER__:function:CreateSQSQueue --payload '{"QueueName": "MyQueue" }' output.txt --profile crossaccount
```