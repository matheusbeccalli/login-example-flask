"""
Database models for the Flask login application.

This module defines the database models using SQLAlchemy ORM,
including the User model with authentication capabilities.
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """
    User model for authentication and user management.
    
    Inherits from UserMixin to provide Flask-Login integration
    and db.Model for SQLAlchemy ORM functionality.
    """
    
    __tablename__ = "users"
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User credentials
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # User status and metadata
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)
    
    def __repr__(self):
        """String representation of the User object."""
        return f"<User {self.username}>"
    
    def set_password(self, password: str) -> None:
        """
        Hash and set the user's password.
        
        Args:
            password (str): The plain text password to hash and store.
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """
        Verify a password against the stored hash.
        
        Args:
            password (str): The plain text password to verify.
        
        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        """
        Return the user ID as a string (required by Flask-Login).
        
        Returns:
            str: The user's ID as a string.
        """
        return str(self.id)
    
    def is_authenticated(self) -> bool:
        """
        Check if the user is authenticated.
        
        Returns:
            bool: True if authenticated, False otherwise.
        """
        return True
    
    def is_anonymous(self) -> bool:
        """
        Check if the user is anonymous.
        
        Returns:
            bool: False for regular users, True for anonymous users.
        """
        return False
    
    def update_last_login(self) -> None:
        """Update the user's last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    @classmethod
    def create_user(cls, username: str, email: str, password: str):
        """
        Create a new user with the provided credentials.
        
        Args:
            username (str): The desired username.
            email (str): The user's email address.
            password (str): The plain text password.
        
        Returns:
            User: The newly created user instance.
        
        Raises:
            ValueError: If username or email already exists.
        """
        # Check if username already exists
        if cls.query.filter_by(username=username).first():
            raise ValueError(f"Username '{username}' already exists")
        
        # Check if email already exists
        if cls.query.filter_by(email=email).first():
            raise ValueError(f"Email '{email}' already exists")
        
        # Create new user
        user = cls(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user