# Flask Login Application

A secure and modern web application demonstrating user authentication with Flask and Bootstrap. This application provides a complete login system with user registration, secure password handling, session management, and a responsive user interface.

## Features

- 🔐 **Secure User Authentication**: Login/logout functionality with Flask-Login
- 🛡️ **Password Security**: Bcrypt password hashing for secure storage
- 🔒 **CSRF Protection**: Form protection against cross-site request forgery
- 📱 **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- 🎨 **Modern UI**: Clean, professional design with Bootstrap components
- 📊 **User Dashboard**: Personal dashboard for authenticated users
- 🚨 **Error Handling**: Comprehensive error pages and logging
- ⚡ **Session Management**: Secure session handling with configurable timeouts
- 📝 **Form Validation**: Client-side and server-side form validation
- 🔍 **Input Sanitization**: Protection against common web vulnerabilities

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLAlchemy ORM with SQLite (easily configurable for other databases)
- **Authentication**: Flask-Login for session management
- **Forms**: Flask-WTF with WTForms for secure form handling
- **Security**: Werkzeug for password hashing, CSRF protection

## Project Structure

```
login example/
├── app/                          # Application package
│   ├── __init__.py              # Application factory
│   ├── models.py                # Database models
│   ├── forms.py                 # WTForms definitions
│   ├── routes/                  # Route blueprints
│   │   ├── main.py             # Main application routes
│   │   └── auth.py             # Authentication routes
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html           # Base template
│   │   ├── index.html          # Home page
│   │   ├── dashboard.html      # User dashboard
│   │   ├── auth/               # Authentication templates
│   │   │   ├── login.html      # Login form
│   │   │   └── register.html   # Registration form
│   │   └── errors/             # Error pages
│   │       ├── 404.html        # Page not found
│   │       └── 500.html        # Server error
│   └── static/                  # Static files
│       ├── css/
│       │   └── style.css       # Custom CSS
│       └── js/
│           └── script.js       # Custom JavaScript
├── logs/                        # Application logs
├── tests/                       # Unit tests
├── config.py                    # Configuration settings
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .env.template               # Environment variables template
└── README.md                   # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download

Download the project files to your local machine.

### Step 2: Create Virtual Environment

```bash
# Navigate to project directory
cd "login example"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

```bash
# Copy environment template
copy .env.template .env

# Edit .env file with your settings (optional for development)
```

### Step 5: Run the Application

```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Usage

### Default Admin Account

For testing purposes, a default admin account is automatically created:

- **Username**: `admin`
- **Password**: `admin123`

### User Registration

1. Navigate to `http://localhost:5000`
2. Click "Register" or "Get Started"
3. Fill in the registration form
4. Submit to create your account

### User Login

1. Go to the login page
2. Enter your username and password
3. Optionally check "Remember Me" for extended sessions
4. Click "Sign In"

### Dashboard Access

Once logged in, users can access their personal dashboard which displays:
- Account information
- Security status
- Session information
- Quick action buttons

## Configuration

### Environment Variables

Create a `.env` file based on `.env.template`:

```bash
# Development settings
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
PORT=5000
LOG_LEVEL=INFO
```

### Production Settings

For production deployment:

1. Set `FLASK_ENV=production`
2. Use a strong, unique `SECRET_KEY`
3. Configure a production database (PostgreSQL, MySQL)
4. Enable HTTPS and update security settings
5. Set up proper logging and monitoring

## Security Features

### Password Security
- Passwords are hashed using Werkzeug's secure password hashing
- Minimum password length requirements
- Password confirmation during registration

### Session Security
- Secure session cookies with HTTPOnly flag
- Configurable session timeouts
- CSRF protection on all forms
- SQL injection prevention through ORM

### Input Validation
- Server-side form validation with WTForms
- Client-side JavaScript validation
- Username and email uniqueness checks
- XSS protection through template escaping

## API Endpoints

### Authentication Routes
- `GET /auth/login` - Display login form
- `POST /auth/login` - Process login credentials
- `GET /auth/register` - Display registration form
- `POST /auth/register` - Process user registration
- `GET /auth/logout` - Logout user

### Main Routes
- `GET /` - Home page
- `GET /dashboard` - User dashboard (requires authentication)

## Customization

### Adding New Features

1. **New Routes**: Create new blueprint files in `app/routes/`
2. **Database Models**: Add models in `app/models.py`
3. **Forms**: Define new forms in `app/forms.py`
4. **Templates**: Add HTML templates in `app/templates/`
5. **Styling**: Modify `app/static/css/style.css`

### Styling Customization

The application uses Bootstrap 5 with custom CSS variables:

```css
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    /* Modify these values to change the theme */
}
```

## Testing

Run the test suite:

```bash
# Install pytest if not already installed
pip install pytest pytest-flask

# Run tests
pytest tests/
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Change the PORT in `.env` file or kill the process using port 5000

2. **Database Issues**
   - Delete `app.db` file and restart the application to recreate the database

3. **Import Errors**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed: `pip install -r requirements.txt`

4. **Template Not Found**
   - Check that all template files are in the correct directories
   - Verify template names match the route handlers

### Logging

Application logs are stored in the `logs/` directory:
- `logs/app.log` - Main application log
- Logs include user actions, errors, and security events

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is provided for educational purposes. Feel free to use and modify as needed.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the application logs
3. Ensure all dependencies are correctly installed
4. Verify environment configuration

## Future Enhancements

- Password reset functionality
- Email verification
- Two-factor authentication
- User profile management
- Social media login integration
- Admin panel for user management
- Rate limiting for login attempts
- Password strength meter