const AWS = require('aws-sdk');

AWS.config.region = 'us-west-1'

function sendSMS(phone, message) {
    const params = {
      Message: message, /* required */
      PhoneNumber: phone,
    };
    
    return new AWS.SNS({apiVersion: '2010-03-31'}).publish(params).promise()
    .catch(error => console.log(error));
}

exports.handler = async (event) => {
    console.log("CUSTOM_CHALLENGE_LAMBDA", event.request);
    
    let secretLoginCode;
    if (!event.request.session || !event.request.session.length) {

        // Generate a new secret login code and send it to the user
        secretLoginCode = Date.now().toString().slice(-4);

        const name = event.request.userAttributes.name
        const message = `Welcome to Just Wipes ${name}!, here is your one time code: ${secretLoginCode}`
        await sendSMS(event.request.userAttributes.phone_number, message);

    } else {

        // re-use code generated in previous challenge
        const previousChallenge = event.request.session.slice(-1)[0];
        secretLoginCode = previousChallenge.challengeMetadata.match(/CODE-(\d*)/)[1];
    }
    
    console.log(event.request.userAttributes);
    
    // Add the secret login code to the private challenge parameters
    // so it can be verified by the "Verify Auth Challenge Response" trigger
    event.response.privateChallengeParameters = { secretLoginCode };

    // Add the secret login code to the session so it is available
    // in a next invocation of the "Create Auth Challenge" trigger
    event.response.challengeMetadata = `CODE-${secretLoginCode}`;
    
    return event;
};