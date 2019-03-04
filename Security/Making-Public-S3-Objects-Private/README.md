# Making Public S3 Objects Private

In this lesson, you'll learn how to detect unintended public access permissions in the ACL of an S3 object and how to revoke them automatically using Lambda, boto3, and CloudWatch Events.

## Create an S3 bucket

```sh
aws s3api create-bucket --bucket everything-must-be-private
aws s3api create-bucket --bucket bucket-for-my-object-level-s3-trail
```

Apply bucket policy:

```sh
aws s3api put-bucket-policy \
--bucket bucket-for-my-object-level-s3-trail \
--policy file://bucket_policy.json
```

## Create a CloudTrail trail and start logging

```sh
aws cloudtrail create-trail \
--name my-object-level-s3-trail \
--s3-bucket-name bucket-for-my-object-level-s3-trail

aws cloudtrail start-logging \
--name my-object-level-s3-trail
```

Create event selectors:

```sh
aws cloudtrail put-event-selectors \
--trail-name my-object-level-s3-trail \
--event-selectors file://event_selectors.json
```

## Create IAM execution role for Lambda

Create IAM role:

```sh
aws iam create-role \
--role-name AllowLogsAndS3ACL \
--assume-role-policy-document file://trust_policy.json
```

Define the access policy:

```sh
aws iam put-role-policy \
--role-name AllowLogsAndS3ACL \
--policy-name AllowLogsAndS3ACL \
--policy-document file://access_policy.json
```

## Create Lambda function

For a `PutObjectAcl` API Event, the function gets the bucket and key name from the event. If the object is not private, then it makes the object private by making a `PutObjectAcl` call.

Zip Lambda function:

```sh
zip -r9 CheckAndCorrectObjectACL.zip lambda_function.py
```

Create Lambda function:

```sh
aws lambda create-function \
--function-name CheckAndCorrectObjectACL \
--zip-file fileb://CheckAndCorrectObjectACL.zip \
--role arn:aws:iam::123456789012:role/AllowLogsAndS3ACL \
--handler lambda_function.lambda_handler \
--runtime python3.7
--environment Variables={BUCKET_NAME=everything-must-be-private}
```

Allow CloudWatch Events to invoke Lambda:

```sh
aws lambda add-permission \
--function-name CheckAndCorrectObjectACL \
--statement-id AllowCloudWatchEventsToInvoke \
--action 'lambda:InvokeFunction' \
--principal events.amazonaws.com \
--source-arn arn:aws:events:us-east-1:123456789012:rule/S3ObjectACLAutoRemediate
```

## Create CloudWatch Events rule

Create rule:

```sh
aws events put-rule \
--name S3ObjectACLAutoRemediate \
--event-pattern file://event_pattern.json
```

Set Lambda function as the target:

```sh
aws events put-targets \
--rule S3ObjectACLAutoRemediate \
--targets Id=1,Arn=arn:aws:lambda:us-east-1:123456789012:function:CheckAndCorrectObjectACL
```

## Testing

```sh
aws s3api put-object \
--bucket everything-must-be-private \
--key MyPersonalInfo

aws s3api get-object-acl \
--bucket everything-must-be-private \
--key MyPersonalInfo
```

The above should return 1 grantee, the owner (you). This indicates that the object is private.

Add public read access, violating our policy:

```sh
aws s3api put-object-acl \
--bucket everything-must-be-private \
--key MyPersonalInfo \
--acl public-read
```

**Quickly check access again:**

```sh
aws s3api get-object-acl \
--bucket everything-must-be-private \
--key MyPersonalInfo
```

You will see another grantee, allowing everyone to read the object:

```json
{
  "Grantee": {
    "Type": "Group",
    "URI": "http://acs.amazonaws.com/groups/global/AllUsers"
  },
  "Permission": "READ"
}
```

Describe the ACL again, and you'll see the Lambda function has removed public read access. Verify in CloudWatch Logs.
