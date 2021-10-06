import logging
import boto3
from botocore.exceptions import ClientError
import os

s3 = boto3.client('s3')

def updateAWS():
    s3.upload_file('file-name.json', 'itlabbucket', 's3_script.json',
                   ExtraArgs={
                       'Metadata':{'Content-Type' : 'json'},
                       'ACL':'public-read',
                       }
                   )

