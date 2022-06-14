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

import json
import os
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns_client = boto3.client('sns')

INVOKE_URL = os.environ['INVOKE_URL']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
  ib_notification = json.loads(event['Records'][0]['Sns']['Message'])

  if ib_notification['state']['status'] != 'AVAILABLE':
    warning_message = 'No action taken. EC2 Image not available.'
    logging.warning(warning_message)
    return {
      'statusCode': 500,
      'body': warning_message
    }

  ami_event = ib_notification['outputResources']['amis'][0]
  ami_name = ami_event['name']
  source_region = ami_event['region']
  image_id = ami_event['image']
  logger.info(f'AMI ID: {image_id}')

  # Publish to SNS topic
  rest_endpoint = f'{INVOKE_URL}?ami={image_id}'
  sns_client.publish(
    TargetArn = SNS_TOPIC_ARN,
    Subject = f'New AMI ({image_id}) has been created, approval required',
    Message = f'AMI Name: {ami_name} has been created\nAMI ID: {image_id} has been created\nRegion: {source_region}\nClick the following link to approve: {rest_endpoint}'
  )
  logger.info('Published to SNS Topic')

  return {
    'statusCode': 200,
    'body': 'Approval email successfully sent'
  }
