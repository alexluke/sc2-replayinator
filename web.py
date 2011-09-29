import os
from flask import Flask, render_template, request
from werkzeug import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
	file = request.files['file']
	filename = secure_filename(f.filename)
	return filename

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.debug = True
	app.run(host='0.0.0.0', port=port)
