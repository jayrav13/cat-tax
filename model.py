# Flask Boilerplate
# By Jay Ravaliya

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

import keys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = keys.MYSQL_KEY

db = SQLAlchemy(app)
db.create_all()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('cats', MigrateCommand)

class Users(db.Model):

	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)
	number = db.Column(db.Text)
	active = db.Column(db.Integer)

	def __init__(self, name, number, active):
		self.name = name
		self.number = number
		self.active = active

class Images(db.Model):

	__tablename__ = "images"

	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.Text)
	image_id = db.Column(db.Text)
	source = db.Column(db.Text)
	is_sent = db.Column(db.Text)

	def __init__(self, url, image_id, source, is_sent):
		self.url = url
		self.image_id = image_id
		self.source = source
		self.is_sent = is_sent

if __name__ == "__main__":
	manager.run()
