import datetime
import os

import boto3

AWS_DEFAULT_REGION = os.environ["AWS_DEFAULT_REGION"]
MAIN_BRANCH_NAME = os.getenv('MAIN_BRANCH_NAME', 'master')
REPOSITORY_NAME = os.environ['REPOSITORY_NAME']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

codecommit = boto3.client('codecommit')
sns = boto3.client('sns')


def get_diff(repository_name, last_commit_id, previous_commit_id):
    differences = []
    response_iterator = None

    paginator = codecommit.get_paginator('get_differences')

    if previous_commit_id is None:
        # This was the first commit (no previous, omit beforeCommitSpecifier)
        response_iterator = paginator.paginate(
            repositoryName=repository_name,
            afterCommitSpecifier=last_commit_id,
        )
    else:
        response_iterator = paginator.paginate(
            repositoryName=repository_name,
            beforeCommitSpecifier=previous_commit_id,
            afterCommitSpecifier=last_commit_id,
        )

    for response in response_iterator:
        differences += response["differences"]

    return differences


def get_diff_change_message_type(change_type):
    type = {
        'M': 'Modification',
        'D': 'Deletion',
        'A': 'Addition'
    }
    return type[change_type]


def get_last_commit_id(repository, branch):
    response = codecommit.get_branch(
        repositoryName=repository,
        branchName=branch
    )
    commit_id = response['branch']['commitId']
    return commit_id


def get_last_commit_log(repository, commit_id):
    response = codecommit.get_commit(
        repositoryName=repository, commitId=commit_id)

    return response['commit']


def get_message_text(differences, last_commit):
    text = ''
    commit_id = last_commit['commitId']
    text += f'commit ID: {commit_id}\n'
    text += 'author: {0} ({1})\n'.format(
        last_commit['author']['name'],
        last_commit['author']['email'])
    date = last_commit['author']['date'].split()[0]
    t_utc = datetime.datetime.utcfromtimestamp(int(date))
    timestamp = t_utc.strftime('%Y-%m-%d %H:%M:%S UTC')
    text += f'date: {timestamp}\n'
    text += f"message: {last_commit['message']}\n"
    for diff in differences:
        if 'afterBlob' in diff:
            text += 'After - File: {0} {1} - Blob ID: {2}\n'.format(
                diff['afterBlob']['path'],
                get_diff_change_message_type(diff['changeType']),
                diff['afterBlob']['blobId'])
        if 'beforeBlob' in diff:
            text += 'Before - File: {0} {1} - Blob ID: {2}\n'.format(
                diff['beforeBlob']['path'],
                get_diff_change_message_type(diff['changeType']),
                diff['beforeBlob']['blobId'])

    text += (f'Commit: '
             f'https://{AWS_DEFAULT_REGION}.console.aws.amazon.com/codesuite/'
             f'codecommit/repositories/{REPOSITORY_NAME}/commit/{commit_id}?'
             f'region={AWS_DEFAULT_REGION}')

    return text


def publish(repository, message):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f'CodeCommit Update - Repository: {repository}',
        Message=message
    )


def lambda_handler(event, context):

    try:
        last_commit_id = get_last_commit_id(REPOSITORY_NAME, MAIN_BRANCH_NAME)
        last_commit = get_last_commit_log(REPOSITORY_NAME, last_commit_id)

        previous_commit_id = None
        if len(last_commit['parents']) > 0:
            previous_commit_id = last_commit['parents'][0]

        print(f'Last commit ID: {last_commit_id}')
        print(f'Previous commit ID: {previous_commit_id}')

        differences = get_diff(
            REPOSITORY_NAME, last_commit_id, previous_commit_id)
        message_text = get_message_text(differences, last_commit)

        print(message_text)

        return publish(REPOSITORY_NAME, message_text)

    except Exception as e:
        import traceback
        print(e)
        traceback.print_exc()
        print(f'Error getting repository {REPOSITORY_NAME}. Ensure it exists '
              'in the same region as this function.')
        raise e
