"""
WTForms for user input validation and CSRF protection.

This module defines all forms used in the application including
login and registration forms with proper validation.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    """
    Login form for user authentication.
    
    Provides fields for username, password, and remember me functionality
    with appropriate validation rules.
    """
    
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required"),
            Length(min=3, max=20, message="Username must be between 3 and 20 characters")
        ],
        render_kw={"placeholder": "Enter your username", "class": "form-control"}
    )
    
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required")
        ],
        render_kw={"placeholder": "Enter your password", "class": "form-control"}
    )
    
    remember_me = BooleanField(
        "Remember Me",
        render_kw={"class": "form-check-input"}
    )
    
    submit = SubmitField(
        "Sign In",
        render_kw={"class": "btn btn-primary w-100"}
    )


class RegistrationForm(FlaskForm):
    """
    Registration form for new user creation.
    
    Provides fields for username, email, password, and password confirmation
    with comprehensive validation including uniqueness checks.
    """
    
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required"),
            Length(min=3, max=20, message="Username must be between 3 and 20 characters")
        ],
        render_kw={"placeholder": "Choose a username", "class": "form-control"}
    )
    
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address")
        ],
        render_kw={"placeholder": "Enter your email", "class": "form-control", "type": "email"}
    )
    
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required"),
            Length(min=6, message="Password must be at least 6 characters long")
        ],
        render_kw={"placeholder": "Create a password", "class": "form-control"}
    )
    
    password2 = PasswordField(
        "Repeat Password",
        validators=[
            DataRequired(message="Please confirm your password"),
            EqualTo("password", message="Passwords must match")
        ],
        render_kw={"placeholder": "Confirm your password", "class": "form-control"}
    )
    
    submit = SubmitField(
        "Register",
        render_kw={"class": "btn btn-primary w-100"}
    )
    
    def validate_username(self, username):
        """
        Custom validator to check username uniqueness.
        
        Args:
            username: The username field to validate.
        
        Raises:
            ValidationError: If the username already exists.
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")
    
    def validate_email(self, email):
        """
        Custom validator to check email uniqueness.
        
        Args:
            email: The email field to validate.
        
        Raises:
            ValidationError: If the email already exists.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")