import logging
from logging.config import dictConfig
import os

from flask import Flask, Blueprint
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import get_config, Config, ProductionConfig
from app.database import db, migrate
from app.routes.routes import register_routes

# Configure logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': get_config().LOG_LEVEL,
        'handlers': ['wsgi']
    }
})

def create_app(config_object=None):
    """
    Application factory for creating Flask app with dynamic configuration.
    
    :param config_object: Optional configuration object
    :return: Configured Flask application
    """
    # Determine configuration based on environment
    if config_object is None:
        env = os.getenv('FLASK_ENV', 'development').lower()
        if env == 'production':
            config_object = ProductionConfig()
        else:
            config_object = Config()
    
    # Create Flask application
    app = Flask(__name__)
    
    # Use configuration from config.py or passed config
    app.config.from_object(config_object)
    if app.config['FLASK_ENV'] == 'production':
        app.logger.setLevel(logging.INFO)
    else:
        app.logger.setLevel(logging.DEBUG)
        # Dev debugging info
        print("Dev debugging info:\n")
        print(f'Running in {app.config["FLASK_ENV"]} mode')
        print(f'Using database: {app.config["SQLALCHEMY_DATABASE_URI"]}')
        print(f'Using secret key: {app.config["SECRET_KEY"]}')
        print(f'Using app name: {app.config["APP_NAME"]}')
        print(f'Using debug mode: {app.config["DEBUG"]}')
        print(f'Using log level: {app.config["LOG_LEVEL"]}')
        print(f'Using database type: {app.config["DB_TYPE"]}')
        print(f'Using database host: {app.config["DB_HOST"]}')
        print(f'Using database port: {app.config["DB_PORT"]}')
        print(f'Using database user: {app.config["DB_USER"]}')
        print(f'Using database password: {app.config["DB_PASSWORD"]}')
        print(f'Using database name: {app.config["DB_NAME"]}')
        print(f'Using SQLALCHEMY_TRACK_MODIFICATIONS: {app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]}')
    
    # Fix for reverse proxy headers
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Upgrade database
    with app.app_context():
        db.create_all()
    
    # Create API blueprint
    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(
        blueprint, 
        version='1.0', 
        title=config_object.APP_NAME,
        description='Dynamic Flask-RESTX Application'
    )
    
    # Register routes dynamically
    register_routes(api)
    
    # Register blueprint
    app.register_blueprint(blueprint)

    # Register error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': str(error)}, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {'error': str(error)}, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'error': str(error)}, 403
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': str(error)}, 404
    
    @app.errorhandler(500)
    def server_error(error):
        return {'error': str(error)}, 500
    
    # add more error handlers as needed

    # We made it this far, return the app..with a cool graphic
    flask_ascii = """
    K    K        A     TTTTTTTTT  BBBBB    OOOOO    OOOOO    K    K  SSSSS
    K   K        A A        T      B    B  O     O  O     O   K   K   S
    K  K        A   A       T      B    B  O     O  O     O   K  K    S
    KKK        AAAAAAA      T      BBBBB   O     O  O     O   KKK     SSSSSS
    K  K      A       A     T      B    B  O     O  O     O   K  K         S
    K   K    A         A    T      B    B  O     O  O     O   K   K        S
    K    K  A           A   T      BBBBB    OOOOO    OOOOO    K    K   SSSSS

    """
    print(flask_ascii)
    
    return app