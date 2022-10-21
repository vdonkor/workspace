import boto3
from boto3.session import Session

client = boto3.client('sts')

response = client.assume_role(RoleArn=arn, RoleSessionName=session_name)
session = Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                      aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                      aws_session_token=response['Credentials']['SessionToken'])
s3_client = session.client('sts')
