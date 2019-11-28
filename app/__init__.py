import os

from flask import Flask
from flask_compress import Compress
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import config_by_name
import firebase_admin

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
compress = Compress()
default_app = firebase_admin.initialize_app()

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    # Set up extensions
    db.init_app(app)
    compress.init_app(app)
    jwt = JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @jwt.user_claims_loader
    def add_claims_to_access_token(identity):
        return {
            'uid': str(identity)
        }

    # Create app blueprints
    from .helloworld import blueprint as helloworld_api
    app.register_blueprint(helloworld_api, url_prefix='/api')

    from .users import blueprint as user_api
    app.register_blueprint(user_api, url_prefix='/api/users')

    from .question import blueprint as question_api
    app.register_blueprint(question_api, url_prefix='/api/questions')

    from .answer import blueprint as answer_api
    app.register_blueprint(answer_api, url_prefix='/api')

    return app
