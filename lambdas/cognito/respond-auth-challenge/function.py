def lambda_handler(event, context):
  """Respond To Auth Challenge

  """
  challenge = event.get('challenge')
  username = event.get('username')
  session = event.get('session')
  answer = event.get('answer')

  response = cognito_client.respond_to_auth_challenge(
    ClientId='57o90j5o2mio2nq95g9m10le6f',
    ChallengeName=challenge,
    Session=session,    
    ChallengeResponses={
      'USERNAME':username,
      'ANSWER': answer
    }
  )
  return response