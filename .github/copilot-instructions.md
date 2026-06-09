<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Build a REST API - Project Setup Instructions

## Project Overview

This is a Django REST API project with:
- CRUD operations for Books and Authors
- JWT authentication
- Swagger/OpenAPI documentation
- Comprehensive test suite
- Django admin panel

## Environment Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

5. Start development server:
   ```bash
   python manage.py runserver
   ```

## API Access

- **Main API**: http://localhost:8000/api/
- **Swagger Docs**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Admin Panel**: http://localhost:8000/admin/
- **Token Endpoint**: http://localhost:8000/api/token/

## Key Features

- **CRUD Operations**: Full CRUD for Books and Authors
- **Authentication**: JWT-based token authentication
- **Filtering**: Advanced filtering and search capabilities
- **Documentation**: Interactive API documentation
- **Admin Interface**: Django admin for data management
- **Tests**: Comprehensive unit and integration tests

## Project Structure

```
api_project/              # Main project directory
├── api_app/             # Django application
│   ├── models.py        # Book and Author models
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # ViewSets and custom actions
│   ├── admin.py         # Admin configuration
│   └── tests.py         # Test suite
├── settings.py          # Django settings
├── urls.py              # URL routing
└── wsgi.py              # WSGI application
```

## Common Commands

- Run migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Run tests: `python manage.py test`
- Start server: `python manage.py runserver`
- Make migrations: `python manage.py makemigrations`
- Create app: `python manage.py startapp appname`

## Important Notes

- All API write operations (POST, PUT, DELETE) require authentication except user registration
- The default SECRET_KEY should be changed before production deployment
- Database is SQLite by default (suitable for development only)
- CORS is configured for localhost:3000 and localhost:8000

## Dependencies

- Django 4.2.13
- Django REST Framework 3.14.0
- djangorestframework-simplejwt (JWT auth)
- django-cors-headers (CORS support)
- drf-spectacular (API documentation)
