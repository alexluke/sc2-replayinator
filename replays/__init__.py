from flask import Flask
from views import views
import settings

def create_app():
	app = Flask(__name__)
	app.config.from_object(settings)
	app.register_blueprint(views)
	return app

