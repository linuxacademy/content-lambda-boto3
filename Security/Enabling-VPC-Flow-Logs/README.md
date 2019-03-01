# Enabling VPC Flow Logs

[VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html) enable you to capture information about the IP traffic going to and from network interfaces in your VPC.

By default, VPC Flow Logs are not enabled. However, in our scenario, let's say you have a policy that requires they be enabled for any new VPC that gets created in your account.

In this lesson, we will automate the creation of VPC Flow Logs whenever a new VPC is created.

- `lambda_function.py` creates VPC Flow Logs for the VPC ID in the event
- `event-pattern.json` is the CloudWatch Rule event pattern for monitoring the `CreateVpc` API call.
- `test-event.json` is a sample CloudTrail event that can be used with the Lambda function, as it contains the VPC ID

## Create IAM role with permission to log to CloudWatch Logs

Allow the VPC Flow Logs service to assume this role:

```sh
aws iam create-role --role-name VPCFlowLogsRole --assume-role-policy-document file://trust-policy.json
```

**Note the ARN for `VPCFlowLogsRole`.**

Example: `arn:aws:iam::123456789012:role/VPCFlowLogsRole`

Grant this role permission to CloudWatch Logs:

```sh
aws iam put-role-policy --role-name VPCFlowLogsRole --policy-name VPCFlowLogsPolicy --policy-document file://vpc-flow-logs-iam-role.json
```

## Create the Lambda Function

Name: `EnableVPCFlowLogs`  
Runtime: `Python 3.7`  
Role: `Create a custom role` (use `lambda_execution_role.json`)  
Code: `lambda_function.py`

## Create a CloudWatch Event Rule to Trigger Lambda

Select **Event Pattern**.  
Service Name: `EC2`  
Event Type: `AWS API Call via CloudTrail`  
Specific operation(s): `CreateVpc`

Event Pattern:

```json
{
    "source": [
        "aws.ec2"
    ],
    "detail-type": [
        "AWS API Call via CloudTrail"
    ],
    "detail": {
        "eventSource": [
            "ec2.amazonaws.com"
        ],
        "eventName": [
            "CreateVpc"
        ]
    }
}
```

**Add target** and select the `EnableVpcFlowLogs` Lambda function.

Click **Configure details**.

## Create a new VPC

```sh
aws ec2 create-vpc --cidr-block 172.20.0.0/16 --region us-east-2`
```

Wait up to a minute for the CloudWatch rule to invoke the Lambda function.
