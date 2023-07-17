# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 12:37:30 2023

@author: kotha
"""
from datetime import datetime as dt
init_time = dt.now()
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
from time import sleep

# Credentials for Authorization
access_id='XXXXXX'
secret_access_key='XXXXXX'

folder_path = os.path.dirname(os.path.realpath(__file__)) + "\\"
resource_to_use = 'dynamodb'
local_region = 'ap-south-1'
table_name = 'dynamodb-trial-table-for-practice-Connections-Directory'

# Establishing Connection to resource
dynamodb = boto3.resource(resource_to_use, region_name=local_region,
                        aws_access_key_id=access_id, aws_secret_access_key=secret_access_key)

#--------------------------------------------------------------------------------------------#

# Create Table
table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {'AttributeName': 'first_name', 'KeyType': 'HASH'},
        {'AttributeName': 'last_name', 'KeyType': 'RANGE'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'first_name', 'AttributeType': 'S'},
        {'AttributeName': 'last_name', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 20,
        'WriteCapacityUnits': 20
    }
)

# Wait until the table exists.
table.wait_until_exists()
print('{} Table created successfully!!'.format(table_name))

# Exploring the Table
table = dynamodb.Table(table_name)
print("Table Creation  Date and Time --->", table.creation_date_time)
print("Number of Items in Table --->", table.item_count)

#--------------------------------------------------------------------------------------------#

# Write Single Record into Table
table.put_item(Item={
    'first_name': 'Dhruv',
    'last_name': 'Kothari',
    'age': 20,
    'gender':'M',
    'relation': 'Brother',
    'contact_number': '9347356743'
    })
print('Single Record Entry done into {} Table successfully!!'.format(table_name))

# Wait for a second
sleep(1)
# print("Number of Items in Table -->", table.item_count) # Does Not gives the Live Count

#--------------------------------------------------------------------------------------------#

# Write Multiple Records into Table with single API Hit
with table.batch_writer(overwrite_by_pkeys=['first_name', 'last_name']) as batch:
    batch.put_item(Item={
            'first_name': 'Pawan',
            'last_name': 'Kumar',
            'age': 26,
            'gender':'M',
            'relation': 'Friend',
            'contact_number': '9871539562'
        }
    )
    batch.put_item(Item={
            'first_name': 'Nisha',
            'last_name': 'Khandelwal',
            'age': 24,
            'gender':'F',
            'relation': 'Friend',
            'contact_number': '9249259255'
        }
    )
    batch.put_item(Item={
            'first_name': 'Mukesh',
            'last_name': 'Jain',
            'age': 50,
            'gender':'M',
            'relation': 'Father',
            'contact_number': '8529462448'
        }
    )
    batch.put_item(Item={
            'first_name': 'Geeta',
            'last_name': 'Kumari',
            'age': 23,
            'gender':'F',
            'relation': 'Friend',
            'contact_number': '9264859672'
        }
    )
    batch.delete_item(Key={
            'first_name': 'Geeta',
            'last_name': 'Kumari',
        }
    )
print('Multiple Records Entry done into {} Table successfully!!'.format(table_name))

#--------------------------------------------------------------------------------------------#

# Update Record in Table 
# Note - Key Attributes cannot be updated from here
response = table.update_item(
    Key={
        'first_name': 'Pawan',
        'last_name': 'Kumar'
    },
    UpdateExpression='SET age = :temp_var',
    ExpressionAttributeValues={
        ':temp_var': 20
    }
)
print('Record Updated into {} Table successfully!!'.format(table_name))

#--------------------------------------------------------------------------------------------#

# Read a Record from Table
response = table.get_item(
    Key={
        'first_name': 'Pawan',
        'last_name': 'Kumar'
    }
)
read_item = response['Item']
print(read_item)

#--------------------------------------------------------------------------------------------#

# Delete Single Record from Table
response = table.delete_item(
    Key={
        'first_name': 'Pawan',
        'last_name': 'Kumar'
    }
)
print('Record Deleted from {} Table successfully!!'.format(table_name))

#--------------------------------------------------------------------------------------------#

# Querying Using Key 
# Note - Partition Key in Mandatory in Key whereas Sort Key is Optional
response = table.query(
    KeyConditionExpression=Key('first_name').eq('Mukesh') & Key('last_name').eq('Jain')
)
items = response['Items']
print("Result --->", items)

# Scanning Using Attributes 
# Note - Can be done using Key also and Sorting Key Alone also can be used
response = table.scan(
    FilterExpression=Attr('first_name').begins_with('D') & Attr('age').gt(10)
)
items = response['Items']
print("Result --->", items)

#--------------------------------------------------------------------------------------------#

# Delete the Table
response = table.delete()
print('{} Table Deleted successfully!!'.format(table_name))

fin_time = dt.now()
print("Code Execution completed in --->", fin_time-init_time)
