# Responding to Invalid SSH Logins

In this lesson, we'll explore a real-world scenario where an EC2 instance is experiencing multiple failed SSH logins, and we want to automatically take the instance offline in response to this potential security event.

Use the Web Server Log Group and the Invalid SSH Login metric filter to trigger a CloudWatch alarm set for 2 data points within 1 minute.

This alarm should publish to an alarm notification SNS topic and send you an email as well as trigger the Lambda function to stop the instance.

## Configure EC2 Instance

EC2 instance must have an IAM role which can communicate with both CloudWatch and Systems Manager.

### Create IAM Instance Role

IAM > Create Role > AWS Service > EC2 > Next: Permissions

Select `CloudWatchAgentAdminPolicy` managed policy.

Select `AmazonEC2RoleforSSM` managed policy.

Name the role `CloudWatchAgentAdminRole`.

### Launch EC2 Instance

Select **Amazon Linux 2**.

Create or select a security group with SSH (port 22) open to the public (`0.0.0.0/0`).

### Attach the IAM Role to the Instance

Assign the `CloudWatchAgentAdminRole` IAM role to the EC2 instance.

### Install CloudWatch Agent using Systems Manager

Run command: `AWS-ConfigureAWSPackage`  
Action: `Install`  
Name: `AmazonCloudWatchAgent`  

### Configure the CloudWatch Agent

Run the CloudWatch Agent Configuration Wizard.

Create a new session using SSM Session Manager.

```sh
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```

**Note: Do not select CollectD, unless you already installed it using `sudo yum install collectd`.**

Specify `/var/log/secure` for "Do you want to monitor any log files?"

### Validate the configuration

```sh
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s
```

## Create SNS Topic

The CloudWatch Alarm will notify this topic, and the topic will trigger the Lambda function.

Topic name: `AlarmNotificationTopic`

## Configure CloudWatch Alarm

### Add a metric filter to the web server log group

Click `secure` log group.

Click **Create metric filter**.

Filter pattern: `[Mon, day, timestamp, ip, id, status = Invalid*]`

Click **Test pattern**.

Click **Assign metric**.

Filter name: `InvalidSSHLogin`

Metric namespace: `SSH`

Metric name: `InvalidSSHLogin`

Click **Create filter**.

### Create Alarm

Metric filter: SSH/InvalidSSHLogin

Click **Create alarm**.

Name: `InvalidSSHLoginAlarm`  
Description: `Invalid login attempts >2 in 1 min for instance <append instance ID>`

**Note: The description is critical, as the instance ID at the end is used by the Lambda function to stop the instance.**

Whenever `InvalidSSHLogin` >= `2` for 1 out of 1 datapoints

### Subscribe to SNS Topic

Select `AlarmNotificationTopic` and click **Create alarm**.

## Create IAM Role for Lambda Function

Create role `LambdaStopInstances` using policy `lambda_execution_role.json`.

## Create Lambda function

Name: `StopInstance`  
Role: `StopInstancesRole`  

### Trigger Lambda from SNS

Trigger > SNS > `AlarmNotificationTopic`

## Trigger the CloudWatch Alarm

Make 3 invalid SSH login attempts within 2 minutes.

Observe that the `secure` log contains the `Invalid user` string.

Observe that the CloudWatch alarm is set.

Observe that the CloudWatch Log for the Lambda function ran.

Observe that the EC2 instance is stopped.
