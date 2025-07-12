from flask import Flask
from .views import views

SECRET_KEY = 'POIEWRSOIHFSLKDJF'
SESSIONS_DATA = {}

def create_app():
    """Initializes and configures the Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_is_safe for your_secret_is_safe in your_secrets'
    app.register_blueprint(views, url_prefix='/')

    return app