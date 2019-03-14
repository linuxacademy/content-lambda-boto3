import pkg_resources


def lambda_handler(event, context):
    pkgs = pkg_resources.working_set
    pkgs_list = sorted([f'{i.key}=={i.version}' for i in pkgs])
    print("\n".join(pkgs_list))

# Log output will resemble:

# START RequestId: 430a0232-8c13-4788-90e0-c24e7ac3d7c4 Version: $LATEST
# boto3==1.9.42
# botocore==1.12.42
# docutils==0.14
# jmespath==0.9.3
# pip==18.1
# python-dateutil==2.7.5
# s3transfer==0.1.13
# setuptools==40.6.2
# six==1.11.0
# urllib3==1.24.1
# END RequestId: 430a0232-8c13-4788-90e0-c24e7ac3d7c4
# REPORT RequestId: 430a0232-8c13-4788-90e0-c24e7ac3d7c4	Duration: 39.76 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 70 MB
