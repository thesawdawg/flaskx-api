from app import create_app
import logging
import os
import sys
import multiprocessing

def run_gunicorn(app):
    """
    Run the application using Gunicorn in production mode.
    
    :param app: Flask application instance
    :return: None
    """
    from gunicorn.app.base import BaseApplication

    class FlaskApplication(BaseApplication):
        def __init__(self, flask_app, options=None):
            self.options = options or {}
            self.application = flask_app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                      if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    # Gunicorn configuration options
    options = {
        'bind': '0.0.0.0:8000',
        'workers': multiprocessing.cpu_count() * 2 + 1,
        'worker_class': 'gthread',
        'threads': 4,
        'worker_tmp_dir': '/dev/shm',  # Use shared memory for worker temp files
        'timeout': 120,
        'keepalive': 5,
        'log_level': 'info',
        'capture_output': True,
        'enable_stdio_inheritance': True,
    }

    FlaskApplication(app, options).run()

def main():
    """
    Runs the Flask application.
    Supports both development and production environments.
    """
    app = create_app()
    
    if app.config['FLASK_ENV'] == 'production':
        # Run in production mode
        app.logger.setLevel(logging.INFO)
        run_gunicorn(app)
    else:
        # Run in development mode
        app.logger.setLevel(logging.DEBUG)
        
        app.run(
            host='0.0.0.0', 
            port=5000, 
            debug=app.config['DEBUG']
        )

if __name__ == '__main__':
    main()
