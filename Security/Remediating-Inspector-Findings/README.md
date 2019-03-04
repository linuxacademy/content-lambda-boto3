# Remediating Inspector Findings

Common Vulnerabilities and Exposures (CVE): <https://cve.mitre.org>

## EC2 Instance Role

Policy: `arn:aws:iam::aws:policy/AmazonSSMFullAccess`

## Lambda Execution Role

Policies:

* `arn:aws:iam::aws:policy/AmazonSSMFullAccess`
* `arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole`

Additional statement for Inspector:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "inspector:DescribeFindings"
      ],
      "Resource": "*"
    }
  ]
}
```

## SNS Topic

Create an SNS topic.

Grant the regional Inspector account permission to publish to the SNS topic.

These users are listed here: <https://docs.aws.amazon.com/inspector/latest/userguide/inspector_assessments.html#sns-topic>

Examples:

* US East (Northern Virginia) - `arn:aws:iam::316112463485:root`
* US East (Ohio) - `arn:aws:iam::646659390643:root`

## Lambda Function

Adapted from <https://github.com/awslabs/amazon-inspector-auto-remediate>.

The Lambda function will automatically patch EC2 instances when an Inspector assessment generates a CVE finding.

The function requires that the EC2 instance to be patched have the Systems Manager (SSM) agent installed, and the agent must have a role attached with necessary SSM permissions. For details on this, see <https://docs.aws.amazon.com/systems-manager/latest/APIReference/Welcome.html>.

### SNS Trigger

The Lambda function is triggered by an SNS notification of a new finding from Inspector. The function checks to make sure that the finding is a CVE missing patch finding, and if so, it checks to ensure tha the SSM agent is running. It then uses SSM to issue the appropriate patch-and-reboot commands to either Ubuntu or Amazon Linux.

## Run Inspector

Ensure that you've tagged the EC2 instance(s) you want to scan.

### Create Assessment Target

1. Click **Create**
2. Choose a name
3. Use tags, selecting the EC2 instance(s) you've tagged for inspection.
4. Click **Save**

### Create Assessment Template

1. Click **Create**
2. Choose a name, i.e. "All Assessments"
3. Select the Assessment Target created in the previous step
4. Select all rules packages
5. Duration: 1 hour
6. Select the SNS topic created previously
7. Deselect **Assessment Schedule**
8. Click **Create and run**

### Assessment Runs

Watch the assessment run progress, periodically refreshing for the full hour to update the **Findings** count.

If there are any findings, check the CloudWatch Log for the Lambda function to observe that SSM ran the update script against the EC2 instance. For example, `yum update -q -y; yum upgrade -y`.

