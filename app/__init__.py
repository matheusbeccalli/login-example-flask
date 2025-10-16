"""
Flask application factory and initialization.

This module contains the application factory function that creates and configures
the Flask application instance with all necessary extensions and blueprints.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_name=None):
    """
    Application factory function that creates and configures a Flask application.
    
    Args:
        config_name (str): The name of the configuration to use.
                          Defaults to 'development' if not specified.
    
    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Determine configuration
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Validate production configuration
    if config_name == "production" and not os.environ.get("SECRET_KEY"):
        raise ValueError("SECRET_KEY environment variable must be set in production")
    
    # Initialize extensions with app
    db.init_app(app)
    csrf.init_app(app)
    
    # Configure Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"
    
    # Import models to ensure they're registered with SQLAlchemy
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login."""
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if it doesn't exist
        if not User.query.filter_by(username="admin").first():
            admin_user = User(username="admin", email="admin@example.com")
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()
            app.logger.info("Created default admin user (username: admin, password: admin123)")
    
    # Configure logging
    configure_logging(app)
    
    return app


def configure_logging(app):
    """
    Configure application logging with rotating file handler.
    
    Args:
        app (Flask): The Flask application instance.
    """
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        logs_dir = os.path.dirname(app.config["LOG_FILE"])
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Set up rotating file handler
        file_handler = RotatingFileHandler(
            app.config["LOG_FILE"],
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        # Set log format
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
        )
        file_handler.setFormatter(formatter)
        
        # Set log level
        log_level = getattr(logging, app.config["LOG_LEVEL"].upper())
        file_handler.setLevel(log_level)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(log_level)
        app.logger.info("Flask login application startup")