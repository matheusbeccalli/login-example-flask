"""
Authentication routes and views.

This module contains all authentication-related routes including
login, logout, and registration functionality.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse as url_parse
from app import db
from app.models import User
from app.forms import LoginForm, RegistrationForm

# Create authentication blueprint
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login functionality.
    
    GET: Display the login form.
    POST: Process login credentials and authenticate user.
    
    Returns:
        Response: Rendered login template or redirect to next page.
    """
    # Redirect if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            # Find user by username
            user = User.query.filter_by(username=form.username.data).first()
            
            # Verify user exists and password is correct
            if user and user.check_password(form.password.data):
                # Log the user in
                login_user(user, remember=form.remember_me.data)
                
                # Update last login timestamp
                user.update_last_login()
                
                current_app.logger.info(f"User {user.username} logged in successfully")
                flash("Login successful!", "success")
                
                # Redirect to next page or home
                next_page = request.args.get("next")
                if not next_page or url_parse(next_page).netloc != "":
                    next_page = url_for("main.index")
                
                return redirect(next_page)
            else:
                current_app.logger.warning(f"Failed login attempt for username: {form.username.data}")
                flash("Invalid username or password", "error")
        
        except Exception as e:
            current_app.logger.error(f"Login error: {str(e)}")
            flash("An error occurred during login. Please try again.", "error")
    
    return render_template("auth/login.html", title="Sign In", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """
    Handle user logout functionality.
    
    Returns:
        Response: Redirect to home page after logout.
    """
    username = current_user.username
    logout_user()
    current_app.logger.info(f"User {username} logged out")
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("main.index"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Handle user registration functionality.
    
    GET: Display the registration form.
    POST: Process registration data and create new user.
    
    Returns:
        Response: Rendered registration template or redirect to login page.
    """
    # Redirect if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            # Create new user
            user = User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            
            current_app.logger.info(f"New user registered: {user.username}")
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("auth.login"))
        
        except ValueError as e:
            current_app.logger.warning(f"Registration failed: {str(e)}")
            flash(str(e), "error")
        
        except Exception as e:
            current_app.logger.error(f"Registration error: {str(e)}")
            flash("An error occurred during registration. Please try again.", "error")
    
    return render_template("auth/register.html", title="Register", form=form)