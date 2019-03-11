# Building a Contact Form with API Gateway and SES

This lesson demonstrates a web page with a typical contact form. Using API Gateway and a Lambda function as a backend for this form, we will send the form post contents via email using SES, and also write the contact data to DynamoDB.

## DynamoDB

Create table `Contact` with primary partition key `id`:

```sh
aws dynamodb create-table --table-name Contact \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode=PAY_PER_REQUEST
```

## Lambda function

Create function **ContactEmail**

## API Gateway

Create API **ContactEmailAPI**

### Create Method

Select **POST** and check the check mark  

Integration Type: Lambda Function  
Use Lambda Proxy Integration: Checked (stores request data in `event`)  
Lambda region: Same region as Lambda function  
Lambda function: **ContactEmail**

### Enable CORS

Select the **POST** method  
Under **Actions** select **Enable CORS**  
Leave the default options and click on **Enable CORS and replace existing CORS headers**.  
Click **Yes, replace existing values**

### Deploy API

Under **Actions** select **Deploy API**  
Deployment stage: **[New stage]**  
Stage name: **prod**  

Note the **Invoke URL** and update `form.js`.

## Test locally

```sh
cd Contact-Form
python3 -m http.server
```

Browse <http://localhost:8000>