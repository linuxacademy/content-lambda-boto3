# Finding Outdated Instance Types

In this lesson, we'll create a custom AWS Config rule to find outdated EC2 instance types. Moving off these old instance types could save on costs and improve performance.

## Create Lambda Function

Create a role called **LambdaCheckInstanceTypeRole** and specify **AWS Config Rules permissions** as the policy template.

Create the Lambda function **CheckInstanceType**. Note the ARN for the next steps.

## Create AWS Config Rule

1. In the AWS Config console, select Rules, then click the **Add rule** button.
2. Next, select **Add custom rule**.
3. Name: **DesiredInstanceTypes**
4. Description: **Checks that all EC2 instances are of the type specified**
5. Select the **AWS Lambda function ARN**, i.e. `arn:aws:lambda:us-east-1:123456789012:function:CheckInstanceType`
6. Trigger type: **Configuration changes**
7. Scope of changes: **Resources**
8. Resources: **EC2: Instance**
9. Rule parameters:
   - Key: `desiredInstanceType`
   - Value: `t2.micro` or a comma-separated list, i.e. `t2.micro,t3.micro`. Any values **not** in this list will have the effect of **noncompliant**.
10. Click **Save**