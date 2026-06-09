# Build a REST API

A comprehensive Django REST API with CRUD operations, JWT authentication, and interactive documentation.

## 🚀 Features

- **CRUD Operations**: Create, Read, Update, Delete operations for Books and Authors
- **User Management**: User registration and profile management
- **JWT Authentication**: Secure token-based authentication
- **API Documentation**: Interactive Swagger UI and ReDoc documentation
- **Filtering & Search**: Advanced filtering, searching, and ordering capabilities
- **Custom Actions**: Special endpoints for book ratings, stock management, and more
- **CORS Support**: Cross-Origin Resource Sharing enabled
- **Admin Panel**: Django admin interface for easy data management
- **Comprehensive Tests**: Unit tests and integration tests included

## 📋 Project Structure

```
Build-a-REST-API/
├── api_project/              # Main Django project
│   ├── api_app/             # Django app with models, views, serializers
│   │   ├── models.py        # Database models (Book, Author)
│   │   ├── serializers.py   # DRF serializers
│   │   ├── views.py         # ViewSets for API endpoints
│   │   ├── admin.py         # Django admin configuration
│   │   └── tests.py         # Test cases
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── __init__.py
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

### Step 1: Clone the Repository

```bash
git clone https://github.com/MadhuKosuri1/Build-a-REST-API.git
cd Build-a-REST-API
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional but Recommended)

```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation

Once the server is running, access the documentation at:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Authentication

The API uses JWT (JSON Web Token) authentication.

#### Obtaining Tokens

**POST** `/api/token/`

Request:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Response:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refreshing Access Token

**POST** `/api/token/refresh/`

Request:

```json
{
  "refresh": "your_refresh_token"
}
```

#### Using Access Token

Include the token in the Authorization header:

```
Authorization: Bearer your_access_token
```

## 🔌 API Endpoints

### Authors

| Method | Endpoint                   | Description        | Auth Required |
| ------ | -------------------------- | ------------------ | ------------- |
| GET    | `/api/authors/`            | List all authors   | No            |
| POST   | `/api/authors/`            | Create new author  | Yes           |
| GET    | `/api/authors/{id}/`       | Get author details | No            |
| PUT    | `/api/authors/{id}/`       | Update author      | Yes           |
| DELETE | `/api/authors/{id}/`       | Delete author      | Yes           |
| GET    | `/api/authors/{id}/books/` | Get author's books | No            |

### Books

| Method | Endpoint                        | Description         | Auth Required |
| ------ | ------------------------------- | ------------------- | ------------- |
| GET    | `/api/books/`                   | List all books      | No            |
| POST   | `/api/books/`                   | Create new book     | Yes           |
| GET    | `/api/books/{id}/`              | Get book details    | No            |
| PUT    | `/api/books/{id}/`              | Update book         | Yes           |
| DELETE | `/api/books/{id}/`              | Delete book         | Yes           |
| POST   | `/api/books/{id}/set_rating/`   | Set book rating     | Yes           |
| POST   | `/api/books/{id}/toggle_stock/` | Toggle stock status | Yes           |
| GET    | `/api/books/top_rated/`         | Get top-rated books | No            |
| GET    | `/api/books/available/`         | Get available books | No            |

### Users

| Method | Endpoint           | Description              | Auth Required |
| ------ | ------------------ | ------------------------ | ------------- |
| POST   | `/api/users/`      | Register new user        | No            |
| GET    | `/api/users/me/`   | Get current user profile | Yes           |
| GET    | `/api/users/{id}/` | Get user details         | Yes           |
| PUT    | `/api/users/{id}/` | Update user              | Yes           |

## 📖 Usage Examples

### Create a Book

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "The Great Gatsby",
    "author_id": 1,
    "description": "A classic American novel",
    "isbn": "9780743273565",
    "publication_date": "1925-04-10",
    "pages": 180,
    "price": 12.99
  }'
```

### Get Books with Filtering

```bash
# Filter by author
curl http://localhost:8000/api/books/?author=1

# Filter by stock status
curl http://localhost:8000/api/books/?in_stock=true

# Search by title
curl http://localhost:8000/api/books/?search=gatsby

# Order by rating (descending)
curl http://localhost:8000/api/books/?ordering=-rating
```

### Get Top-Rated Books

```bash
curl http://localhost:8000/api/books/top_rated/?limit=5
```

### Set Book Rating

```bash
curl -X POST http://localhost:8000/api/books/1/set_rating/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"rating": 4.5}'
```

## 🧪 Running Tests

```bash
python manage.py test
```

To run tests with verbose output:

```bash
python manage.py test --verbosity=2
```

To run specific test class:

```bash
python manage.py test api_project.api_app.tests.BookTestCase
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication with token expiration
- **CORS Configuration**: Configured for specified origins only
- **Permission Classes**: Role-based access control
- **Secure Password Hashing**: Django's built-in password hashing
- **Input Validation**: Serializer validation on all inputs

## 📝 Environment Variables

Create a `.env` file in the project root (optional):

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## 🚀 Deployment

### For Production

1. Set `DEBUG=False` in settings.py
2. Update `SECRET_KEY` with a secure value
3. Configure `ALLOWED_HOSTS` appropriately
4. Use a production database (PostgreSQL recommended)
5. Set up HTTPS
6. Use a production server (Gunicorn, uWSGI)

## 📦 Dependencies

- **Django 4.2.13**: Web framework
- **Django REST Framework 3.14.0**: RESTful API framework
- **djangorestframework-simplejwt 5.3.2**: JWT authentication
- **django-cors-headers 4.3.1**: CORS handling
- **drf-spectacular 0.26.5**: API documentation generation

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

- **Madhu Kosuri** - Initial work - [GitHub](https://github.com/MadhuKosuri1)

## 🆘 Support

For support, open an issue on the GitHub repository or contact the maintainers.

## 🎯 Roadmap

- [ ] Add pagination customization
- [ ] Implement rate limiting
- [ ] Add email notifications
- [ ] Implement caching with Redis
- [ ] Add API versioning
- [ ] Create Docker configuration
- [ ] Add CI/CD pipeline with GitHub Actions

---

**Last Updated**: 2026-06-09

**API Version**: 1.0.0
