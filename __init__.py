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

@app.route("/", methods=['GET','POST'])
def home():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		if 'name' not in request.form or 'phone-number' not in request.form:
			return render_template('index.html', message="Hmm - something went wrong with the form. Try it again!")
		elif len(request.form['name']) == 0:
			return render_template('index.html', message="Uh oh! Enter a name!")
		elif len(request.form['phone-number']) != 12:
			return render_template('index.html', message="Uh oh! The phone number has to be 12 characters - 10 numbers separated by 2 dashes!")
		else:
			user = Users(request.form['name'], request.form['phone-number'], 0)
			db.session.add(user)
			db.session.commit()
			return render_template('index.html', message="")


@app.route('/api/v0.1/message', methods=['GET'])
def message():
	resp = twilio.twiml.Response()
	resp.message("Test").media('http://25.media.tumblr.com/tumblr_m4n449Twri1qea9rlo1_400.gif')
	return str(resp)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
