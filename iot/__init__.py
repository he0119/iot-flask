""" All Flask extensions are created here
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
login_manager = LoginManager()
jwt = JWTManager()


def create_app(config):
    """ Return a Flask App.
    """
    app = Flask(__name__,
                instance_path=config.INSTANCE_PATH,
                instance_relative_config=True)
    app.config.from_object(config)
    app.config.from_pyfile('application.cfg', silent=True)

    db.init_app(app)
    migrate.init_app(app, db, directory='instance/migrations')
    socketio.init_app(app, cors_allowed_origins='*')
    login_manager.init_app(app)
    jwt.init_app(app)

    swaggerui_blueprint = get_swaggerui_blueprint(
        app.config.get('SWAGGER_URL'), app.config.get('SWAGGER_API_URL'))
    from iot.api.api import api_bp
    from iot.frontend.controllers import frontend_bp

    app.register_blueprint(frontend_bp, url_prefix='')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(swaggerui_blueprint,
                           url_prefix=app.config.get('SWAGGER_URL'))

    return app
