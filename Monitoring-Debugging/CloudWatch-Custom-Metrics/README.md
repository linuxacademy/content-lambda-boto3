# Publishing Custom Metrics from Lambda

Install the demo app using the [AWS Serverless Application Model](https://aws.amazon.com/serverless/sam/)

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

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.
1. Choose the AWS CloudFormation stack that you created in the preceding step from the list shown\.
1. Under **Outputs**, note the API Gateway endpoint URLs.
1. Browse each and observe the JSON responses.

## Generate Traffic

Using the API Gateway endpoint URLs in the previous step, generate load against each of these endpoints.

Modify `URLs.txt` to use the endpoint URLs in your account.

Run [Apache Bench](http://httpd.apache.org/docs/2.4/programs/ab.html) using [parallel](http://www.gnu.org/software/parallel/):

```sh
cat URLs.txt | parallel 'ab -c 350 -n 20000 {}'
```

## View Custom Metrics