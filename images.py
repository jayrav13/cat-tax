from model import db, Users, Images
import requests
from lxml import html
from twilio.rest import TwilioRestClient
import os
from datetime import datetime
from clarifai.client import ClarifaiApi

def send_image():
	image = Images.query.filter_by(is_sent=0).first()

	if image == None:
		parameters = {
			"format" : "xml",
			"results_per_page" : "100"
		}
		result = requests.get('http://thecatapi.com/api/images/get', params=parameters)
		tree = html.document_fromstring(result.text)

		clarifai_api = ClarifaiApi()

		for val in tree.xpath('//images'):
			for elem in val:
				try:
					result = clarifai_api.tag_image_urls(elem.xpath('url')[0].text)
					total_results = result['results'][0]['result']['tag']['classes']
					if 'cat' in total_results or 'kitten' in total_results:
						db.session.add(Images(elem.xpath('url')[0].text, elem.xpath('id')[0].text, elem.xpath('source_url')[0].text, 0))
						db.session.commit()
				except:
					pass

		image = Images.query.filter_by(is_sent=0).first()

	users = Users.query.filter_by(active=1).all()

	for elem in users:
		client = TwilioRestClient(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
		message = client.messages.create(to=elem.number, from_="+19733214779", media_url=[image.url])

	image.is_sent = 1
	db.session.commit()

dt = datetime.now()

if dt.hour >= 9 and dt.hour <= 17:
	send_image()
