# Rotating IAM Access Keys

Lambda function that revokes user access keys periodically to enforce rotation and mitigate risk.

Lambda function:

- Collects IAM users using pagination
- Scans each user for existing IAM Access keys
- Deactivates the keys
- Sends email alert to administrator

Scheduled CloudWatch trigger:

- Triggers the Lambda to run, i.e. weekly