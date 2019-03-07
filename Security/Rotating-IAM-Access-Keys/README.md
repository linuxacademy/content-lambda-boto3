# Rotating IAM Access Keys

Lambda function that revokes user access keys periodically to enforce rotation and mitigate risk.

Lambda function:

- Collects IAM users using pagination
- Scans each user for existing IAM Access keys older than 90 days
- Deactivates the keys
- Sends email alert to administrator

Scheduled CloudWatch Rule:

- Triggers the Lambda to run, i.e. weekly

## Amazon Simple Email Service (Amazon SES)

Be sure to use an [SES-verified email address](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html) to ensure properly delivery of emails.

SES API endpoints are not available in all regions. See [here](https://docs.aws.amazon.com/general/latest/gr/rande.html#ses_region) for a list of supported endpoints.
