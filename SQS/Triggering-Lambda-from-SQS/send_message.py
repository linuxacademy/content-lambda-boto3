#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import argparse
import logging
import sys
from time import sleep

import boto3
from faker import Faker

parser = argparse.ArgumentParser()
parser.add_argument("--queue-name", "-q", required=True,
                    help="SQS queue name")
parser.add_argument("--interval", "-i", required=True,
                    help="timer interval", type=float)
parser.add_argument("--message", "-m", help="message to send")
parser.add_argument("--log", "-l", default="INFO",
                    help="logging level")
args = parser.parse_args()

if args.log:
    logging.basicConfig(
        format='[%(levelname)s] %(message)s', level=args.log)

else:
    parser.print_help(sys.stderr)

sqs = boto3.client('sqs')

response = sqs.get_queue_url(QueueName=args.queue_name)

queue_url = response['QueueUrl']

logging.info(queue_url)

while True:
    message = args.message
    if not args.message:
        fake = Faker()
        message = fake.text()

    logging.info('Sending message: ' + message)

    response = sqs.send_message(
        QueueUrl=queue_url, MessageBody=message)

    logging.info('MessageId: ' + response['MessageId'])
    sleep(args.interval)
