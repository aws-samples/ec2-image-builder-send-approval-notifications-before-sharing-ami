# Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client('ec2')
sns_client = boto3.client('sns')

TARGET_ACCOUNT_IDS = os.environ['TARGET_ACCOUNT_IDS']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):

  image_id = event['queryStringParameters']['ami']
  logger.info(f'AMI ID: {image_id}')

  response = ec2.modify_image_attribute(
    ImageId=image_id,
    OperationType='add',
    Attribute='launchPermission',
    UserIds=TARGET_ACCOUNT_IDS.split(",")
  )
  logger.info('AMI Shared')

  # Send success email to target account email address
  sns_client.publish(
    TargetArn = SNS_TOPIC_ARN,
    Subject = f'New AMI ({image_id}) has been successfully shared',
    Message = f'AMI ID: {image_id}\n\nTarget Accounts: {TARGET_ACCOUNT_IDS}\n\nA new AMI ({image_id}) has been created and successfully shared with the accounts above.\n\nThank you.'
  )
  logger.info('Published to SNS Topic')

  return {
    'statusCode': 200,
    'body': 'Successfully shared AMI'
  }
