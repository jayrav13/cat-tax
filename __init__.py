# Flask Boilerplate
# By Jay Ravaliya

from flask import Flask, make_response, jsonify, request, abort, render_template, redirect
from flask.ext.assets import Environment, Bundle
import requests
import twilio.twiml

from model import db, Users, Images

app = Flask(__name__)

assets = Environment(app)
css = Bundle('css/bootstrap.min.css', 'css/styles.css', output='get/packed.css')
assets.register('css_all', css)
js = Bundle('js/jquery.js', 'js/bootstrap.min.js', 'js/scripts.js', output='get/packed.js')
assets.register('js_all', js)

@app.route("/", methods=['GET'])
def home():
	return render_template('index.html')


@app.route('/api/v0.1/message', methods=['GET'])
def message():
	if request.values.get('Body', None).strip().lower() == 'register':
		user = User(request.values.get('From'))
		db.session.add(user)
		db.session.commit()
		resp = twilio.twiml.Response()
		resp.message("Confirmed! Stay tuned for cat pics!")
		return str(resp)
	elif request.values.get('Body', None).strip().lower() == 'stop':
		user = Users.query.filter_by(number=request.values.get('From')).first()
		if not user:
			resp = twilio.twiml.Response()
			resp.message("Hmm - you're not in our system! Want to receive cat pics? Reply with \"register\"")
			return str(resp)
		else:
			user.active = 0
			db.session.commit()
			resp = twilio.twiml.Response()
			resp.message("You won't get any more messages - for now. Reply with \"resume\" to start receiving again.")
			return str(resp)
	else:
		resp = twilio.twiml.Response()
		resp.message("Sorry - I don't understand that command!")
		return str(resp)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
