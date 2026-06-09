# Django REST API - Quick Start Guide

## Project Setup and Running

### 1. Prerequisites

- Python 3.8+
- pip
- Virtual environment (venv)

### 2. Installation Steps

#### Step 1: Navigate to Project

```bash
cd Build-a-REST-API
```

#### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Step 5: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

#### Step 6: Start Development Server

```bash
python manage.py runserver
```

### 3. Access Points

Once the server is running:

- **API Root**: http://localhost:8000/api/
- **Swagger Documentation**: http://localhost:8000/api/docs/
- **ReDoc Documentation**: http://localhost:8000/api/redoc/
- **Admin Panel**: http://localhost:8000/admin/
- **Get Token**: POST http://localhost:8000/api/token/

### 4. Get Started with API

#### Create a User Account

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123"
  }'
```

#### Get Access Token

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepass123"
  }'
```

Copy the `access` token from the response.

#### Create an Author

```bash
curl -X POST http://localhost:8000/api/authors/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "J.K. Rowling",
    "email": "jk@example.com",
    "bio": "Famous author"
  }'
```

#### Create a Book

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Harry Potter and the Philosopher'\''s Stone",
    "author_id": 1,
    "description": "A magical journey",
    "isbn": "9780439708180",
    "publication_date": "1998-06-26",
    "pages": 309,
    "price": 15.99
  }'
```

#### Get All Books

```bash
curl http://localhost:8000/api/books/
```

#### Get Top-Rated Books

```bash
curl http://localhost:8000/api/books/top_rated/?limit=5
```

### 5. Running Tests

```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific test class
python manage.py test api_project.api_app.tests.BookTestCase
```

### 6. Key Endpoints Summary

**Authentication:**

- POST `/api/token/` - Get access token
- POST `/api/token/refresh/` - Refresh access token

**Books:**

- GET `/api/books/` - List books
- POST `/api/books/` - Create book (authenticated)
- GET `/api/books/{id}/` - Get book detail
- PUT `/api/books/{id}/` - Update book (authenticated)
- DELETE `/api/books/{id}/` - Delete book (authenticated)
- POST `/api/books/{id}/set_rating/` - Set rating (authenticated)
- POST `/api/books/{id}/toggle_stock/` - Toggle stock (authenticated)
- GET `/api/books/top_rated/` - Get top-rated books
- GET `/api/books/available/` - Get available books

**Authors:**

- GET `/api/authors/` - List authors
- POST `/api/authors/` - Create author (authenticated)
- GET `/api/authors/{id}/` - Get author detail
- PUT `/api/authors/{id}/` - Update author (authenticated)
- DELETE `/api/authors/{id}/` - Delete author (authenticated)
- GET `/api/authors/{id}/books/` - Get author's books

**Users:**

- POST `/api/users/` - Register user
- GET `/api/users/me/` - Get current user (authenticated)
- GET `/api/users/{id}/` - Get user detail (authenticated)
- PUT `/api/users/{id}/` - Update user (authenticated)

### 7. Useful Django Commands

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Access Django shell
python manage.py shell

# Clear database
python manage.py flush
```

### 8. Troubleshooting

**Port Already in Use:**

```bash
python manage.py runserver 8001
```

**Clear Cache:**

```bash
# Clear migrations
rm -r api_project/api_app/migrations/
# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

**Database Reset:**

```bash
# Delete database
rm db.sqlite3

# Run migrations
python manage.py migrate

# Create superuser again
python manage.py createsuperuser
```

### 9. Project Structure

```
Build-a-REST-API/
├── api_project/
│   ├── api_app/
│   │   ├── __init__.py
│   │   ├── admin.py         # Admin configuration
│   │   ├── apps.py          # App configuration
│   │   ├── models.py        # Database models
│   │   ├── serializers.py   # DRF serializers
│   │   ├── views.py         # ViewSets and views
│   │   └── tests.py         # Test suite
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI app
├── manage.py                # Management script
├── requirements.txt         # Dependencies
├── README.md               # Project README
└── .gitignore             # Git ignore rules
```

### 10. Next Steps

1. Add more models as needed
2. Implement additional serializers
3. Add custom viewset actions
4. Configure database for production (PostgreSQL)
5. Deploy to production server
6. Set up CI/CD pipeline

---

For more details, check the README.md file or visit the GitHub repository.
