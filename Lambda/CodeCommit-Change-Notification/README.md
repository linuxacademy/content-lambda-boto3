# Automating CodeCommit Change Notifications

In this lesson, we'll demonstrate how to receive detailed email notifications
about file changes and commit messages when a code update is pushed to
CodeCommit. A code reviewer may subscribe to the SNS topic and recieve updates
for any changes.

## Create the CodeCommit Repository

```sh
aws codecommit create-repository --repository-name ChangeNotification
```

Note the `cloneUrlHttp` and `Arn` values in the response.

## Create and Subscribe to the SNS Topic

```sh
aws sns create-topic --name CodeCommitChangeNotification

aws sns subscribe \
--topic-arn arn:aws:sns:us-east-1:123456789012:CodeCommitChangeNotification \
--protocol email \
--notification-endpoint my-email@example.com
```

## Create IAM Lambda Execution Role

1. Add `AWSLambdaBasicExecutionRole`
2. Add the following policy `LambdaCodeCommitSnsPolicy`:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
            "codecommit:*",
            "sns:*"
            ],
            "Resource": "*"
        }]
    }
    ```

## Create the Lambda Function

Name: **CodeCommitChangeNotification**

Set the following enviornment variables:

`REPOSITORY_NAME` = `ChangeNotification`

`SNS_TOPIC_ARN` = `arn:aws:sns:us-east-1:123456789012:CodeCommitChangeNotification`

## Create the CloudWatch Event Rule

This rule will detect branch or repository changes:

1. Choose **Event Pattern**.
2. Service Name: **CodeCommit**
3. Event Type: **CodeCommit Repository State Change**
4. Specific resource(s) by ARN: **CodeCommit Repository ARN**

    Select the **referenceCreated** and **referenceUpdated** events.

    Event Pattern:

    ```json
    {
    "source": [
        "aws.codecommit"
    ],
    "detail-type": [
        "CodeCommit Repository State Change"
    ],
    "resources": [
        "arn:aws:codecommit:us-east-1:123456789012:ChangeNotification"
    ]
    }
    ```

5. Target: **CodeCommitChangeNotification**

## Commit a Change

1. Create and commit a file.
2. Edit the file and commit it.