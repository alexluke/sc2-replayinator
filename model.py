from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///tmp/test.db'
db = SQLAlchemy(app)

class Replay(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	key = db.Column(db.String(20), unique=True)
	hash = db.Column(db.String(40), unique=True)
	filename = db.Column(db.String(255))

	def __init__(self, filename, hash):
		self.filename = filename
		self.hash = hash
		self.key = self.create_unique_key()
	
	def create_unique_key(self):
		existing = self.query.filter_by(hash=self.hash).first()
		if existing:
			return existing.key

		length = 6
		key = self.hash[0:length]
		while query.filter_by(key=key).count() > 0:
			length += 1
			if length > 40:
				break;
			key = self.hash[0:length]
		return key
