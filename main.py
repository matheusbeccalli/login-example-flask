"""
Main application entry point.

This module serves as the entry point for the Flask application,
creating the application instance and running the development server.
"""

import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Create the application instance
app = create_app()

if __name__ == "__main__":
    """
    Run the Flask development server.
    
    This should only be used for development. In production,
    use a proper WSGI server like Gunicorn or uWSGI.
    """
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )