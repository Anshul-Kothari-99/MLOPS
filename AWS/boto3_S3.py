# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 20:35:44 2023

@author: Anshul Kothari
"""

import boto3
import os
from time import sleep

# Credentials for Authorization
access_id='XXXXXX'
secret_access_key='XXXXXX'

folder_path = os.path.dirname(os.path.realpath(__file__)) + "\\"
file_name = 'test.png'
resource_to_use = 's3'
local_region = 'ap-south-1'
bucket_name = 's3-trial-bucket-for-practice'

# Establishing Connection to resource
s3 = boto3.client(resource_to_use, aws_access_key_id=access_id, aws_secret_access_key=secret_access_key)

# Create Bucket
location = {'LocationConstraint': local_region}
response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
print("{} bucket Created successfully!!".format(bucket_name))

# Wait for sometime
sleep(7)

# List existing available buckets
buckets = s3.list_buckets()
bucket_name = buckets['Buckets'][0]['Name']

# For Uploading File
response = s3.upload_file(folder_path+"images\\"+file_name, bucket_name, file_name)
print("{} file Uploaded successfully!!".format(file_name))

# Wait for sometime
sleep(7)

# For Downloading File
response = s3.download_file(bucket_name, file_name, folder_path+file_name)
print("{} file Downloaded successfully!!".format(file_name))

# Wait for sometime
sleep(7)

# For Deleting File
response = s3.delete_object(Bucket=bucket_name, Key=file_name)
print("{} file Deleted successfully!!".format(file_name))

# Wait for sometime
sleep(7)

# For Deleting Bucket
response = s3.delete_bucket(Bucket=bucket_name)
print("{} bucket Deleted successfully!!".format(bucket_name))