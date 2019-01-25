# Triggering Lambda from SQS

Run the provided script `send_message.py` to send messages to SQS

**Example**: Send a message containing random text to the `Messages` queue every 0.1 second (10 messages per second):

`./send_message.py -q Messages -i 0.1`

Press `Ctrl+C` to quit.
