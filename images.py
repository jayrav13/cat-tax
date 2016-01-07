from model import db, Users, Images
import requests
from lxml import html
from twilio.rest import TwilioRestClient
import os
import datetime

def send_image():
	image = Images.query.filter_by(is_sent=0).first()

	if image == None:
		parameters = {
			"format" : "xml",
			"results_per_page" : "100"
		}
		result = requests.get('http://thecatapi.com/api/images/get', params=parameters)
		tree = html.document_fromstring(result.text)

		for val in tree.xpath('//images'):
			for elem in val:
				db.session.add(Images(elem.xpath('url')[0].text, elem.xpath('id')[0].text, elem.xpath('source_url')[0].text, 0))
				db.session.commit()

		image = Images.query.filter_by(is_set=0).first()

	users = Users.query.filter_by(active=1).all()

	for elem in users:
		client = TwilioRestClient(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
		message = client.messages.create(to=elem.number, from_="+19733214779", media_url=[image.url])

	image.is_sent = 1
	db.session.commit()

dt = datetime.datetime.now()
if dt[3] >= 9 and dt[3] <= 17:
	send_image()
