from imgurpython import ImgurClient
from clarifai.client import ClarifaiApi
from model import db, Images, Users
from twilio.rest import TwilioRestClient
from datetime import datetime
import os

def send_message():
	image = Images.query.filter_by(is_sent=0).first()

	if image == None:
		imgur_client = ImgurClient(os.environ.get('IMGUR_CLIENT_ID'), os.environ.get('IMGUR_CLIENT_SECRET'))
		clarifai_api = ClarifaiApi()

		images = imgur_client.subreddit_gallery(subreddit='aww', page=0)

		for image in images:
			if image.is_album == False and ('jpeg' in image.type):
				try:
					result = clarifai_api.tag_image_urls(image.link)
					total_result = result['results'][0]['result']['tag']['classes']
					if len(set(total_result).intersection(['dog', 'puppy', 'cat', 'kitten', 'bird'])) > 0:
						db.session.add(Images(image.link))
						db.session.commit()
				except:
					pass

		image = Images.query.filter_by(is_sent=0).first()

	users = Users.query.filter_by(active=1).all()

	for user in users:
		client = TwilioRestClient(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
		message  = client.messages.create(to=user.number, from_="+19733214779", media_url=[image.link])
		
	image.is_sent = 1
	db.session.commit()

dt = datetime.now()

if dt.hour >= 9 and dt.hour <= 18:
	send_message()
