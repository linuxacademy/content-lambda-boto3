# Stopping EC2 Instances Nightly

Be sure to set the Lambda function timeout high enough (i.e. 1 minute) so that it can iterate through every instance in every region.