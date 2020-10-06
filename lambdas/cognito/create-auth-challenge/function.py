import random
import string
import boto3

def handler(event, context):
  """Create Challenge and then Send Notification
  """
  response = event.get('response')
  request = event.get('request')
  session = request.get('session')
  if (not session) or len(session) == 0:
    letters = string.ascii_letters
    secretLoginCode = ''.join(random.choice(letters) for i in range(6))#call_your_create_otp_fn()  # create OTP here

    # send Notification
    contact = request.get('userAttributes').get('phone_number')
    # << call_your notify_fn_here()
    client = boto3.client('sns')
    client.publish(Message='Here ya mF code {}'.format(secretLoginCode), PhoneNumber=contact)
  else:
    previousChallenge = session[0]
    secretLoginCode = previousChallenge.get('challengeMetadata')
    response.update({
      'privateChallengeParameters': {'answer': secretLoginCode},
      'challengeMetadata': secretLoginCode,
      'publicChallengeParameters': {
        'answer': secretLoginCode
        }
    })
  return event