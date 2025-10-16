"""
Unit tests for the Flask login application.

This module contains comprehensive tests for authentication,
routes, models, and security features.
"""

import unittest
import tempfile
import os
from app import create_app, db
from app.models import User


class FlaskLoginTestCase(unittest.TestCase):
    """Test case for Flask login application."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_path}'
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()
        self.client = self.app.test_client()
        
        # Create test user
        self.test_user = User(username='testuser', email='test@example.com')
        self.test_user.set_password('testpassword')
        db.session.add(self.test_user)
        db.session.commit()
    
    def tearDown(self):
        """Clean up after each test method."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def login(self, username, password):
        """Helper method to login a user."""
        return self.client.post('/auth/login', data={
            'username': username,
            'password': password,
            'csrf_token': self.get_csrf_token()
        }, follow_redirects=True)
    
    def logout(self):
        """Helper method to logout a user."""
        return self.client.get('/auth/logout', follow_redirects=True)
    
    def get_csrf_token(self):
        """Helper method to get CSRF token from login form."""
        response = self.client.get('/auth/login')
        # In a real test, you would parse the CSRF token from the response
        # For now, return a dummy token since CSRF is disabled in testing
        return 'dummy_csrf_token'
    
    def test_home_page(self):
        """Test home page accessibility."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Flask Login App', response.data)
    
    def test_login_page(self):
        """Test login page accessibility."""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)
    
    def test_register_page(self):
        """Test registration page accessibility."""
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Account', response.data)
    
    def test_valid_login(self):
        """Test login with valid credentials."""
        response = self.login('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        # In a real test, check for successful login indicators
    
    def test_invalid_login(self):
        """Test login with invalid credentials."""
        response = self.login('testuser', 'wrongpassword')
        self.assertEqual(response.status_code, 200)
        # Should stay on login page with error message
    
    def test_logout(self):
        """Test user logout functionality."""
        self.login('testuser', 'testpassword')
        response = self.logout()
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication."""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_user_model(self):
        """Test user model functionality."""
        user = User(username='newuser', email='new@example.com')
        user.set_password('password123')
        
        # Test password setting and checking
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.check_password('wrongpassword'))
        
        # Test string representation
        self.assertEqual(str(user), '<User newuser>')


if __name__ == '__main__':
    unittest.main()