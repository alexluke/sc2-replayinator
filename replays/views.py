import os
from flask import Blueprint, render_template, request, redirect, url_for
from hashlib import sha1
import model

views = Blueprint('views', __name__, static_folder='../static', template_folder='../templates')

@views.route('/')
def home():
	latest = []
	for replay in model.Replay.query.all():
		latest.append({
			'name': replay.original_filename,
			'link': url_for('.replay', key=replay.key),
		})
	
	return render_template('home.html', latest=latest)

@views.route('/replay/<key>/')
def replay(key):
	replay = model.Replay.query.filter_by(key=key).one()
	return render_template('replay.html', replay=replay)

@views.route('/replay/<key>/download/')
def replay_download(key):
	replay = model.Replay.query.filter_by(key=key).one()
	return redirect(replay.download_url())

@views.route('/submit', methods=['POST'])
def submit():
	file = request.files['file']
	hash = sha1(file.read()).hexdigest()
	replay = model.Replay(file.filename, hash)

	if model.Replay.query.filter_by(key=replay.key).count() > 0:
		return redirect(url_for('.replay', key=replay.key))

	replay.upload(file)
	model.db.session.add(replay)
	model.db.session.commit()
	return redirect(url_for('.replay', key=replay.key))

@views.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404

