# Publishing Custom Metrics from Lambda

Install the demo app using the [AWS Serverless Application Model](https://aws.amazon.com/serverless/sam/). You can find instructions to install the AWS SAM CLI [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).

## Create the Lambda deployment package

`cd shopping-cart-app`

Create an S3 bucket in the location where you want to save the packaged code. If you want to use an existing S3 bucket, skip this step.

```sh
aws s3 mb s3://123456789012-shopping-cart-app
```

Create the deployment artifacts with dependencies

```sh
sam build
```

Create the Lambda function deployment package by running the following `package` AWS SAM CLI command at the command prompt.

```sh
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket 123456789012-shopping-cart-app
```

In the AWS SAM CLI, use the `deploy` command to deploy all of the resources that you defined in the template.

```sh
sam deploy \
    --template-file packaged.yaml \
    --stack-name shopping-cart-app \
    --capabilities CAPABILITY_IAM
```

## Locate API Gateway Endpoint URLs

1. Open the AWS CloudFormation console at <https://console.aws.amazon.com/cloudformation>.
1. Choose the AWS CloudFormation stack that you created in the preceding step from the list shown\.
1. Under **Outputs**, note the API Gateway endpoint URLs.
1. Browse each and observe the JSON responses.

## Generate Traffic

Using the API Gateway endpoint URLs in the previous step, generate traffic against each of these endpoints.

Run an HTTP testing tool like [vegeta](https://github.com/tsenart/vegeta) to generate traffic to your API gateway endpoints:

Modify `URLs.txt` to use the endpoint URLs in your account.

Run a test for 60 minutes:

```sh
cat URLS.txt | vegeta attack -duration=60m | tee results.bin | vegeta report
```

## View Custom Metrics

You may view custom metric data while a load test is in progress.

1. Open the CloudWatch console at <https://console.aws.amazon.com/cloudwatch>.
1. Navigate to **Metrics**.
1. Under **All metrics**, select **ShoppingCartApp**.
1. Select **Metrics with no dimensions**.
1. Select **ItemsAddedToCart**, **OrderTotal**, and **ViewProduct**.
