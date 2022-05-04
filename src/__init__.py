from flask import Flask, jsonify
from src.auth import auth
from src.users import users
from src.posts import posts
from src.database import db
from src.config.appconfig import DevelopmentConfig
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config


def create_app(app_config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(app_config)

    if DevelopmentConfig.SECRET_KEY == 'development':
        SWAGGER = {
            'title': "Bookmarks API",
            'uiversion': 3
        }

    db.app = app
    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    Swagger(app, config=swagger_config, template=template)

    @app.get("/")
    def home():
        return {"message": "This is home page"}

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error": "Page not found"}), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"error": "Something went wrong. We are working on it"}), 500

    return app
