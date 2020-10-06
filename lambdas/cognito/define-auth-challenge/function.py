def handler(event, context):
  """Define Auth Challenge Trigger
  """
  response = event.get('response')
  request = event.get('request')
  session = request.get('session')

  current_session = len(session) - 1
  print('response',response)
  print('request', request)
  print('session', session)
  # # If user is not registered
  if request.get('userNotFound') is True:
    print('userNotFound')
    response.update({
      'issueTokens': False,
      'failAuthentication': True,+
      'msg': "User does not exist"
    })
      
  # wrong OTP even After 3 sessions?
  elif len(session) >=3 and session[2].get('challengeResult') is False:
    print('wrong OTP even After 3 sessions?')
    response.update({
      'issueTokens': False,
      'failAuthentication': True
    })
  # Correct OTP!
  elif len(session) > 0 and session[current_session].get('challengeResult') is True:
    print('Correct OTP!')
    response.update({
      'issueTokens': True,
      'failAuthentication': False
    })
  # not yet received correct OTP
  else:
    print('not yet received correct OTP')
    response.update({
      'issueTokens': False,
      'failAuthentication': False,
      'challengeName': 'CUSTOM_CHALLENGE'
    })

  return  event