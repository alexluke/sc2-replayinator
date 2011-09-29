import os
from flask import Flask, render_template, request, redirect, url_for
from hashlib import sha1
import model

app = Flask(__name__)

@app.route('/')
def home():
	latest = []
	for replay in model.Replay.query.all():
		latest.append({
			'name': replay.original_filename,
			'link': url_for('replay', key=replay.key),
		})
	
	return render_template('home.html', latest=latest)

@app.route('/replay/<key>')
def replay(key):
	replay = model.Replay.query.filter_by(key=key).one()
	return replay.original_filename

@app.route('/submit', methods=['POST'])
def submit():
	file = request.files['file']
	hash = sha1(file.read()).hexdigest()
	replay = model.Replay(file.filename, hash)

	if model.Replay.query.filter_by(key=replay.key).count() > 0:
		return redirect(url_for('replay', key=replay.key))

	replay.upload(file)
	model.db.session.add(replay)
	model.db.session.commit()
	return redirect(url_for('replay', key=replay.key))

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.debug = True
	app.run(host='0.0.0.0', port=port)
