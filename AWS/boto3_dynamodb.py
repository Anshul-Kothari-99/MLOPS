# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 12:37:30 2023

@author: kotha
"""
import boto3
import os
from time import sleep

# Credentials for Authorization
access_id='XXXXXX'
secret_access_key='XXXXXX'

folder_path = os.path.dirname(os.path.realpath(__file__)) + "\\"
resource_to_use = 'dynamodb'
local_region = 'ap-south-1'
table_name = 'dynamodb-trial-table-for-practice'

# Establishing Connection to resource
dynamodb = boto3.client(resource_to_use, aws_access_key_id=access_id, aws_secret_access_key=secret_access_key)