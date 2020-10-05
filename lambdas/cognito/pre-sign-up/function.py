def lambda_handler(event, context):
  event['response']['autoConfirmUser'] = True
  event['response']['autoVerifyPhone'] = True
  return event