# Automating Resource Tagging

Automate the tagging of EC2 instances and their corresponding resources using a Lambda function with CloudTrail and CloudWatch. The function will ensure that users can work only on those resources that they have created based on resource tags. This is enforced via an IAM policy.

## Create the IAM Policy

This policy allows Start/Stop/Reboot/Terminate for EC2 instances where the tag 'Owner' matches the current requester's user ID.

```sh
aws iam create-policy \
--policy-name TagBasedEC2RestrictionsPolicy \
--policy-document file://TagBasedEC2RestrictionsPolicy.json
```

Note the policy ARN.

## Attach IAM Policy to Group

Create a group called **developers**:

```sh
aws iam create-group --group-name developers
```

Attach the policy to the group:

```sh
aws iam attach-group-policy \
--policy-arn arn:aws:iam::123456789012:policy/TagBasedEC2RestrictionsPolicy \
--group-name developers
```

## Create IAM Role for Lambda Function

Create IAM role:

```sh
aws iam create-role \
--role-name LambdaAllowTaggingEC2Role \
--assume-role-policy-document file://trust_policy.json
```

Define the access policy:

```sh
aws iam put-role-policy \
--role-name LambdaAllowTaggingEC2Role \
--policy-name LambdaAllowTaggingEC2Policy \
--policy-document file://access_policy.json
```

## Create Lambda Function

Create function `TagEC2Resources`.

## Create CloudWatch Rule

Create rule:

```sh
aws events put-rule \
--name AutoTagResources \
--event-pattern file://event_pattern.json
```

Set Lambda function as the target:

```sh
aws events put-targets \
--rule AutoTagResources \
--targets Id=1,Arn=arn:aws:lambda:us-east-2:123456789012:function:TagEC2Resources
```

## Create EC2 Instance as User

Create an EC2 instance as an administrative/root user. Observe the `Owner` tag.

Try working with EC2 instances owned by other users or untagged, and observe access denied errors.

## What next?

Now that you know you can tag resources with a Lambda function in response to events, you can apply the same logic to other resources such as RDS databases or S3 buckets. With resource groups, each user can focus on just their resources, and the IAM policy provided in this lesson assures that no unauthorized action is possible on someone else's instance.

Additionally, tags are useful in custom billing reports to project costs and determine how much money each individual owner is spending. You can activate the `Owner` tag in the billing console from the Cost Allocation Tags of your billing console to include it in your detailed billing reports. For more information, see [Applying Tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-what-is.html).