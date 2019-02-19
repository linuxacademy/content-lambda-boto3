# Facial Recognition

To extract the detected face names from the response JSON at the command line:

```sh
`jq '.CelebrityFaces[].Name' response.json` > names.txt
```

More info on `jq` is [here](https://stedolan.github.io/jq/).
