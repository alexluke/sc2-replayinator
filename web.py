import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from hashlib import sha1
import model

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/replay/<key>')
def replay(key):
	replay = model.Replay.query.filter_by(key=key).one()
	return replay.filename

@app.route('/submit', methods=['POST'])
def submit():
	file = request.files['file']
	hash = sha1(file.read()).hexdigest()
	replay = model.Replay(secure_filename(file.filename), hash)

	if model.Replay.query.filter_by(key=replay.key).count() > 0:
		return redirect(url_for('replay', key=replay.key))

	model.db.session.add(replay)
	model.db.session.commit()
	return replay.key

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.debug = True
	app.run(host='0.0.0.0', port=port)
