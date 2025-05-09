from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = 'secretul_tau_este_in_siguranta'

    from .views import views
    app.register_blueprint(views, url_prefix= '/')

    return app
