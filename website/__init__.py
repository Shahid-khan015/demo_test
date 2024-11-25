from flask import Flask


def create_app():
    app = Flask(__name__)
  

    from .view import views
    from .api import api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/')

    return app

