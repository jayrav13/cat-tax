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
manager.add_command('imgur', MigrateCommand)

class Users(db.Model):

	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.Text)
	active = db.Column(db.Integer)

	def __init__(self, number):
		self.number = number
		self.active = 1

class Images(db.Model):

	__tablename__ = "images"

	id = db.Column(db.Integer, primary_key=True)
	link = db.Column(db.Text)
	is_sent = db.Column(db.Integer)

	def __init__(self, link):
		self.link = link
		self.is_sent = 0

if __name__ == "__main__":
	manager.run()
