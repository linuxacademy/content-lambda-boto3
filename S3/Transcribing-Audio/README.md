# Transcribing Audio

To extract the raw text transcript from the JSON file at the command line:

```sh
jq '.results.transcripts[0].transcript' -r asrOutput.json > transcript.txt
```

More info on `jq` is [here](https://stedolan.github.io/jq/).