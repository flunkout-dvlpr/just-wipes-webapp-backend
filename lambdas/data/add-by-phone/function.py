import boto3
import json
from datetime import datetime

def get_user_data(s3, s3_bucket, phone_number):
  try:
    object_name = '{}.json'.format(phone_number)
    userFile = s3.get_object(Bucket=s3_bucket, Key=object_name)
    user_data = json.loads(userFile['Body'].read().decode('utf-8'))
    return user_data
  except s3.exceptions.NoSuchKey as e:
    print('File Does Not Exist!')
    return False

def handler(event, context):
  body = json.loads(event['body'])
  phone_number = body.get('phone_number')
  phone_number = phone_number.replace('+1', '')
  purchase = body.get('purchase')

  s3 = boto3.client('s3')
  s3_bucket = "just-wipes"
  
  user_data = get_user_data(s3, s3_bucket, phone_number)
  print(user_data)

  if len(user_data['purchases']) != 0:
    purchaseIds = [purchase['id'] for purchase in user_data['purchases']]
    if purchase['id'] not in purchaseIds:
      user_data['purchases'].append(purchase)
    else:
      print('Sorry this purchase has already been redeemed!')
      return {
        'statusCode': 200,
        'headers': {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps( {
          "type": "warning",
          "message": "This purchase has already been redeemed!"
        })
      }
  else:
    user_data['purchases'].append(purchase)

  json_data = bytes(json.dumps(user_data).encode('UTF-8'))
  object_name = '{}.json'.format(phone_number)
  s3.put_object(Bucket=s3_bucket, Key=object_name, Body=json_data, ContentType="application/json")

  return {
    'statusCode': 200,
    'headers': {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    },
    "body": json.dumps( {
      "payload": user_data,
      "type": "success",
      "message": "Purchase redeemed, Thank You!"
    })
  }