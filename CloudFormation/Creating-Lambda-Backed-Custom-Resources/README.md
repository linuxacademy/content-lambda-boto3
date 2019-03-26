# Creating Lambda-backed Custom Resources

When you associate a Lambda function with a custom resource, the function is invoked whenever the custom resource is created, updated, or deleted. CloudFormation calls a Lambda API to invoke the function and to pass all the request data (such as the request type and resource properties) to the function.

In this lesson, you will learn how to implement password confirmation logic into a CloudFormation template.

## AWS CloudFormation Deep Dive

<https://linuxacademy.com/cp/modules/view/id/157>

Custom resources are Lambda functions that get called by CloudFormation. CloudFormation has lots of defined resources that you can use to provision AWS resources. However, if you want to provision an AWS resource that CloudFormation doesn't support yet, or if you want to include some complicated logic during your CloudFormation stack create/update/delete, you can use a custom resource to do that easily.

## Create CloudFormation stack

During a stack operation, CloudFormation sends a request to a pre-signed URL with a service token specified in the template, and then waits for a response before proceeding with the stack operation.

The custom resource provider (i.e. Lambda function) processes the CloudFormation request and returns a response of `SUCCESS` or `FAILED` to the pre-signed URL.
