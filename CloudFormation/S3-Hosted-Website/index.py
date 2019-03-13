import json
import mimetypes
import os
import threading
import urllib.request
import zipfile
from urllib.parse import urlparse

import boto3
import cfnresponse

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    print(json.dumps(event))
    response_data = {}
    response_data['Data'] = None

    # Setup timer to catch timeouts
    t = threading.Timer((context.get_remaining_time_in_millis() / 1000.00) - 0.5,
                        timeout, args=[event, context])
    t.start()

    try:
        bucket = event['ResourceProperties']['BucketName']
        repo_subdir = event['ResourceProperties']['RepoSubdir']
        repo_url = event['ResourceProperties']['RepoURL']
        repo_name = urlparse(repo_url).path.split('/')[-2]
        local_file = download_repo(repo_url)
        extract(local_file, '/tmp')
        upload_to_s3(bucket, f'/tmp/{repo_name}-master/{repo_subdir}')
        cfnresponse.send(event, context, cfnresponse.SUCCESS,
                         response_data, "CustomResourcePhysicalID")
    except Exception as e:
        print("Error: " + str(e))
        cfnresponse.send(event, context, cfnresponse.FAILED,
                         response_data, "CustomResourcePhysicalID")
    finally:
        # Cancel timer before exit
        t.cancel()


# Function that executes just before lambda execution times out
def timeout(event, context, logger):
    print("Execution is about to time out, sending failure message")
    cfnresponse.send(event, context, cfnresponse.FAILED,
                     {}, "CustomResourcePhysicalID", reason="Execution timed out")


def download_repo(url):
    # i.e. https://github.com/linuxacademy/content-lambda-boto3/archive/master.zip
    url += 'archive/master.zip'
    print('Downloading repo: ' + url)
    file_name = os.path.basename(url)  # i.e. master.zip
    local_file = os.path.join('/tmp', file_name)
    urllib.request.urlretrieve(url, local_file)
    st = os.stat(local_file)
    print(f'Downloaded {st.st_size} bytes')
    return local_file


def extract(file, target_dir):
    print(f'Extracting {file} to {target_dir}')
    with zipfile.ZipFile(file, "r") as zip:
        zip.printdir()
        zip.extractall(target_dir)


def upload_to_s3(bucket, path):
    print(f'Uploading {path} to s3://{bucket}')
    bucket = s3.Bucket(bucket)
    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            mime_type = mimetypes.MimeTypes().guess_type(full_path)[0]
            with open(full_path, 'rb') as data:
                print(f'Uploading: {full_path} [{mime_type}]')
                bucket.put_object(
                    Key=full_path[len(path)+1:], Body=data, ContentType=mime_type)
