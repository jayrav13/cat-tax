from twilio.rest import TwilioRestClient
import os
import datetime

if datetime.datetime.now().hour == 8:
	client = TwilioRestClient(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
	message = client.messages.create(to="+19738967552", from_="+19733214779", body="This works!")
