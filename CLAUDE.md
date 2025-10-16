# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flask-based web application demonstrating user authentication with SQLAlchemy ORM, Flask-Login session management, and WTForms validation. Uses Bootstrap 5 for responsive UI.

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start development server (default: http://localhost:5000)
python main.py

# The app uses .env file for configuration
# Copy .env.template to .env and modify as needed
```

### Testing
```bash
# Run test suite
pytest tests/

# Run specific test file
pytest tests/test_app.py

# Run with coverage
pytest --cov=app tests/
```

### Database Operations
```bash
# Database is SQLite by default (app.db)
# Tables are created automatically on first run via db.create_all() in app/__init__.py:74
# Default admin user created automatically: username=admin, password=admin123

# To reset database, delete app.db and restart application
```

## Architecture

### Application Factory Pattern
The app uses Flask's application factory pattern (`create_app()` in `app/__init__.py`). This enables:
- Multiple configurations (development, production, testing)
- Easier testing with different configs
- Extension initialization with app context

### Blueprint Structure
Routes are organized into blueprints for separation of concerns:
- **auth_bp** (`app/routes/auth.py`): Authentication routes registered at `/auth` prefix
  - `/auth/login` - User login
  - `/auth/logout` - User logout
  - `/auth/register` - User registration
- **main_bp** (`app/routes/main.py`): Main application routes at root
  - `/` or `/index` - Home page
  - `/dashboard` - User dashboard (requires authentication)

### Database Models
Located in `app/models.py`. The User model includes:
- Werkzeug password hashing (methods: `set_password()`, `check_password()`)
- Flask-Login integration via UserMixin
- Class method `create_user()` for user creation with validation
- Instance method `update_last_login()` for tracking login timestamps

### Forms and Validation
WTForms in `app/forms.py` provide:
- Server-side validation with validators (DataRequired, Email, Length, EqualTo)
- Custom validators for uniqueness checks (`validate_username()`, `validate_email()`)
- Automatic CSRF protection via Flask-WTF
- Bootstrap-ready form rendering with `render_kw` attributes

### Extension Initialization
Extensions are initialized globally in `app/__init__.py` then bound to app:
```python
db = SQLAlchemy()          # Database ORM
login_manager = LoginManager()  # Session management
csrf = CSRFProtect()       # CSRF protection
```

### Configuration Management
Three-tier config in `config.py`:
- **Config**: Base class with common settings (SECRET_KEY, database URI, session config)
- **DevelopmentConfig**: Debug enabled, insecure cookies allowed
- **ProductionConfig**: Debug disabled, secure cookies required, HTTPS expected
- **TestingConfig**: In-memory SQLite, CSRF disabled for testing

Environment selection via `FLASK_ENV` variable (defaults to development).

### Security Features
- Passwords hashed with Werkzeug's `generate_password_hash()`
- CSRF protection on all forms via Flask-WTF
- Session cookies configured with HTTPOnly, SameSite=Lax
- SQL injection prevention through SQLAlchemy ORM
- Login redirects validated to prevent open redirects (see `auth.py:54`)

### Logging
Rotating file handler configured in `app/__init__.py:90-122`:
- Logs stored in `logs/app.log`
- 10MB max size with 10 backup files
- Log level configurable via LOG_LEVEL env variable
- Only active in production (debug=False)

### Template Structure
Templates use Jinja2 with inheritance:
- `base.html` - Base template with Bootstrap layout
- `auth/` - Authentication templates
- `errors/` - Error page templates (404, 500)

## Development Patterns

### Adding New Routes
1. Create route function in appropriate blueprint file
2. Use decorators for authentication (`@login_required`)
3. Use `current_app.logger` for logging
4. Wrap in try-except for error handling
5. Flash messages use categories: 'success', 'error', 'info'

### Adding Database Models
1. Define model class in `app/models.py` inheriting from `db.Model`
2. Import in `app/__init__.py` to register with SQLAlchemy
3. Tables auto-created via `db.create_all()` in app factory

### Creating Forms
1. Define FlaskForm subclass in `app/forms.py`
2. Add validators from wtforms.validators
3. Custom validators as methods: `validate_<field_name>(self, field)`
4. Forms auto-include CSRF token when rendered

### Testing Approach
Tests in `tests/test_app.py` use:
- `create_app('testing')` for test configuration
- Temporary database file per test
- Helper methods for login/logout actions
- CSRF disabled in testing config for simpler test writing

## Important Notes

- Virtual environment is in `venv/` directory (excluded from git)
- SQLite database file `app.db` created in project root
- Session timeout configured in config.py (default: 1 hour)
- User loader function required for Flask-Login (see `app/__init__.py:60-63`)
- Error handlers registered on main_bp blueprint
- URL validation on login redirects prevents open redirect vulnerabilities
- Production deployment requires strong SECRET_KEY and HTTPS
