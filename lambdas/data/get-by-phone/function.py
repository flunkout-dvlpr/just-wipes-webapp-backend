import boto3
import json
from datetime import datetime

def userFileExists(s3, s3_bucket, phone_number):
  try:
    object_name = '{}.json'.format(phone_number)
    userFile = s3.get_object(Bucket=s3_bucket, Key=object_name)
    user_data = json.loads(userFile['Body'].read().decode('utf-8'))
    return user_data
  except s3.exceptions.NoSuchKey as e:
    print('File Does Not Exist, Creating...')
    return False

def createUserFile(s3, s3_bucket, name, phone_number):
  dateTimeObj = datetime.now().isoformat()
  file_structure = { "name": name,
                     "phone_number": '+1' + phone_number,
                     "signUpOn": dateTimeObj,
                     "purchases": []
                   }
  json_data = bytes(json.dumps(file_structure).encode('UTF-8'))
  object_name = '{}.json'.format(phone_number)
  s3.put_object(Bucket=s3_bucket, Key=object_name, Body=json_data, ContentType="application/json")
  s3_bucket_path = 'https://{}.s3.us-east-2.amazonaws.com/{}'.format(s3_bucket, phone_number)
  return file_structure

def handler(event, context):
  body = json.loads(event['body'])
  name = body.get('name')
  phone_number = body.get('phone_number')
  phone_number = phone_number.replace('+1', '')

  s3 = boto3.client('s3')
  s3_bucket = "just-wipes"

  user_data = userFileExists(s3, s3_bucket, phone_number)
  if user_data:
    return {
      'statusCode': 200,
      'headers': {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      "body": json.dumps( {
        "payload": user_data,
        "type": "success"
      })
    }
  else:
    new_user = createUserFile(s3, s3_bucket, name, phone_number)
    return {
      'statusCode': 200,
      'headers': {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      "body": json.dumps( {
        "payload": new_user,
        "type": "success"
      })
    }