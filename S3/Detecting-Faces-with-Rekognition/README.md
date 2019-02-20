# Detecting Faces with Rekognition

## DynamoDB

Create table `Faces` with primary partition key `key`:

```sh
aws dynamodb create-table --table-name Faces \
  --attribute-definitions AttributeName=key,AttributeType=S \
  --key-schema AttributeName=key,KeyType=HASH \
  --billing-mode=PAY_PER_REQUEST
```

## Extracting detected face names from the response JSON

```sh
`jq '.CelebrityFaces[].Name' response.json` > names.txt
```

More info on `jq` is [here](https://stedolan.github.io/jq/).
