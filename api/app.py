from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from .extensions import db, ma
from flask_jwt_extended import JWTManager
from werkzeug.contrib.fixers import ProxyFix

def create_app(localconfig):
    app = Flask(__name__)
    app.config.from_object(localconfig)
    db.init_app(app)
    ma.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    api = Api(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    from .resources import application, user_info

    api.add_resource(
        user_info.StartPage,
        '/start_page'
    )
    api.add_resource(
        application.UserLogin,
        '/login'
    )
    api.add_resource(
        application.UserRegistration,
        '/registration'
    )
    api.add_resource(
        application.TokenRefresh,
        '/token_refresh'
    )
    api.add_resource(
        application.GetUserData,
        '/get_user_data'
    )
    api.add_resource(
        user_info.AccountOptions,
        '/account_options'
    )
    return app
