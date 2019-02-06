# AWS Instance Scheduler

The AWS Instance Scheduler is a solution that automates the starting and stopping of EC2 and RDS instances.

The Instance Scheduler leverages resource tags and Lambda to automatically stop and restart instances across multiple AWS Regions and accounts on a customer-defined schedule.

The solution is easy to deploy and can help reduce operational costs. For example, an organization can use the Instance Scheduler in a non-production environment to automatically stop instances every day, outside of business hours. For customers who leave all of their instances running at full utilization, this solution can result in up to 70% cost savings for those instances that are only necessary during regular business hours (weekly utilization reduced from 168 hours to 50 hours).

## Deployment

Sign in to the AWS Management Console and click the button below to launch the `aws-instance-scheduler.json` AWS CloudFormation template.

[![Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Faws-instance-scheduler%2Flatest%2Finstance-scheduler.template)

You can also [download the template](https://raw.githubusercontent.com/linuxacademy/content-lambda-boto3/master/EC2/AWS-Instance-Scheduler/aws-instance-scheduler.json) as a starting point for your own implementation.
