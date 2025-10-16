"""
Main application routes and views.

This module contains the main application routes including
the home page and other general functionality.
"""

from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_login import current_user

# Create main blueprint
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@main_bp.route("/index")
def index():
    """
    Display the application home page.
    
    Shows different content based on whether the user is authenticated or not.
    
    Returns:
        Response: Rendered home page template.
    """
    try:
        # Log page access
        if current_user.is_authenticated:
            current_app.logger.info(f"User {current_user.username} accessed home page")
        else:
            current_app.logger.info("Anonymous user accessed home page")
        
        return render_template("index.html", title="Home")
    
    except Exception as e:
        current_app.logger.error(f"Error rendering home page: {str(e)}")
        return render_template("errors/500.html"), 500


@main_bp.route("/dashboard")
def dashboard():
    """
    Display the user dashboard (requires authentication).
    
    Returns:
        Response: Rendered dashboard template or redirect to login.
    """
    try:
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        
        current_app.logger.info(f"User {current_user.username} accessed dashboard")
        return render_template("dashboard.html", title="Dashboard")
    
    except Exception as e:
        current_app.logger.error(f"Error rendering dashboard: {str(e)}")
        return render_template("errors/500.html"), 500


@main_bp.errorhandler(404)
def not_found_error(error):
    """
    Handle 404 Not Found errors.
    
    Args:
        error: The error object.
    
    Returns:
        Response: Rendered 404 error template.
    """
    current_app.logger.warning(f"404 error: {error}")
    return render_template("errors/404.html"), 404


@main_bp.errorhandler(500)
def internal_error(error):
    """
    Handle 500 Internal Server errors.
    
    Args:
        error: The error object.
    
    Returns:
        Response: Rendered 500 error template.
    """
    current_app.logger.error(f"500 error: {error}")
    return render_template("errors/500.html"), 500