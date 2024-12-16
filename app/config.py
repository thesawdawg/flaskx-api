import os
from functools import lru_cache

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    # Application Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    APP_NAME = os.getenv('APP_NAME', 'Flask Dynamic App')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    # Database Configuration
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'app_database')

    # Generate SQLAlchemy Database URI
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """
        Dynamically generate database connection string based on configuration.
        Supports SQLite, MySQL, and PostgreSQL.
        """
        db_type = self.DB_TYPE.lower()
        
        if db_type == 'sqlite':
            if not self.DB_NAME:
                raise ValueError("SQLite requires a database name.")
            if self.FLASK_ENV == 'production':
                raise ValueError("SQLite is not supported in production. C'mon, use a real database.")
            
            # Ensure database directory exists
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_directory = os.path.dirname(current_dir)
            database_dir = os.path.join(parent_directory, 'database')
            
            # Create database directory if it doesn't exist
            os.makedirs(database_dir, exist_ok=True)
            
            # Full path to the database file
            db_path = os.path.join(database_dir, f'{self.DB_NAME}.db')
            
            # Ensure the database file exists
            if not os.path.exists(db_path):
                open(db_path, 'w').close()
            
            return f'sqlite:////{db_path}'
        elif db_type == 'mysql':
            if not all([self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME]):
                raise ValueError("MySQL requires host, user, password, and database name.")
            return (
                f'mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@'
                f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
            )
        elif db_type == 'postgresql':
            if not all([self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME]):
                raise ValueError("PostgreSQL requires host, user, password, and database name.")
            return (
                f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@'
                f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
            )
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG

class ProductionConfig(Config):
    """Production configuration settings."""
    # Disable debug mode
    DEBUG = False
    
    # Enable production-level logging
    LOG_LEVEL = 'WARNING'
    
    # Enforce HTTPS in production
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    
    # Prevent CSRF protection bypass
    WTF_CSRF_ENABLED = True
    
    # Strict security headers
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Prevent clickjacking
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Optimize SQLAlchemy for production
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_POOL_TIMEOUT = 30
    
    # Use a strong, randomly generated secret key
    SECRET_KEY = os.getenv('PRODUCTION_SECRET_KEY', os.urandom(32))

@lru_cache()
def get_config():
    """
    Cached configuration getter to avoid reloading environment variables.
    
    :return: Configuration instance
    """
    return Config()
