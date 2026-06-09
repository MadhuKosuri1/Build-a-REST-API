# API Documentation

## Overview

This is a comprehensive REST API for managing books and authors with authentication and documentation. The API follows REST principles and uses JSON for data exchange.

**Base URL:** `http://localhost:8000/api/`

**Documentation:**

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

---

## Authentication

The API uses JWT (JSON Web Token) authentication. All protected endpoints require an `Authorization` header with a bearer token.

### Authentication Flow

#### 1. Register a New User

**Endpoint:** `POST /api/users/`

**Request:**

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password_123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Response (201 Created):**

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "is_staff": false
}
```

#### 2. Obtain Access Token

**Endpoint:** `POST /api/token/`

**Request:**

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password_123"
  }'
```

**Response (200 OK):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 3. Refresh Access Token

**Endpoint:** `POST /api/token/refresh/`

When the access token expires, use the refresh token to get a new one.

**Request:**

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

**Response (200 OK):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Using Access Token

Include the access token in the `Authorization` header for all protected requests:

```bash
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Example:

```bash
curl http://localhost:8000/api/books/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

---

## Endpoints

### Authors Endpoints

#### List All Authors

**GET** `/api/authors/`

Public endpoint - no authentication required.

**Query Parameters:**

- `search`: Search by author name or email
- `ordering`: Sort by field (e.g., `created_at`, `-created_at` for descending)
- `page`: Page number for pagination

**Example:**

```bash
curl "http://localhost:8000/api/authors/?search=rowling&ordering=-created_at"
```

**Response (200 OK):**

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "J.K. Rowling",
      "email": "jk@example.com",
      "bio": "British author",
      "birth_date": "1965-07-31",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create Author

**POST** `/api/authors/`

Requires authentication.

**Request:**

```bash
curl -X POST http://localhost:8000/api/authors/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Stephen King",
    "email": "stephen@example.com",
    "bio": "American novelist",
    "birth_date": "1947-09-21"
  }'
```

**Response (201 Created):**

```json
{
  "id": 2,
  "name": "Stephen King",
  "email": "stephen@example.com",
  "bio": "American novelist",
  "birth_date": "1947-09-21",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

#### Get Author Detail

**GET** `/api/authors/{id}/`

Public endpoint.

**Response (200 OK):**

```json
{
  "id": 1,
  "name": "J.K. Rowling",
  "email": "jk@example.com",
  "bio": "British author",
  "birth_date": "1965-07-31",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Update Author

**PUT** `/api/authors/{id}/`

Requires authentication.

**Request:**

```bash
curl -X PUT http://localhost:8000/api/authors/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "bio": "British author - Updated bio"
  }'
```

**Partial Update (PATCH):**

```bash
curl -X PATCH http://localhost:8000/api/authors/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "bio": "British author - Updated bio"
  }'
```

#### Delete Author

**DELETE** `/api/authors/{id}/`

Requires authentication.

**Response:** 204 No Content

#### Get Author's Books

**GET** `/api/authors/{id}/books/`

Public endpoint - returns all books by the specified author.

**Response (200 OK):**

```json
{
  "count": 7,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Harry Potter and the Philosopher's Stone",
      "author": {...},
      "description": "A magical journey",
      ...
    }
  ]
}
```

---

### Books Endpoints

#### List All Books

**GET** `/api/books/`

Public endpoint.

**Query Parameters:**

- `search`: Search by title, description, ISBN, or author name
- `author`: Filter by author ID
- `in_stock`: Filter by stock status (true/false)
- `rating`: Filter by rating (exact match)
- `ordering`: Sort by field (created_at, rating, price)
- `page`: Page number

**Examples:**

```bash
# Search for books
curl "http://localhost:8000/api/books/?search=harry"

# Filter by author
curl "http://localhost:8000/api/books/?author=1"

# Filter by stock status
curl "http://localhost:8000/api/books/?in_stock=true"

# Sort by rating (descending)
curl "http://localhost:8000/api/books/?ordering=-rating"

# Combine filters
curl "http://localhost:8000/api/books/?author=1&in_stock=true&ordering=-rating"
```

**Response (200 OK):**

```json
{
  "count": 50,
  "next": "http://localhost:8000/api/books/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Harry Potter and the Philosopher's Stone",
      "author": {
        "id": 1,
        "name": "J.K. Rowling",
        "email": "jk@example.com",
        "bio": "British author",
        "birth_date": "1965-07-31",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
      },
      "author_id": 1,
      "description": "The first book in the Harry Potter series",
      "isbn": "9780439708180",
      "publication_date": "1998-06-26",
      "pages": 309,
      "rating": 4.9,
      "price": "15.99",
      "in_stock": true,
      "created_by": 1,
      "created_by_username": "jkrowling",
      "created_at": "2024-01-15T10:35:00Z",
      "updated_at": "2024-01-15T10:35:00Z"
    }
  ]
}
```

#### Create Book

**POST** `/api/books/`

Requires authentication.

**Request:**

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Harry Potter and the Chamber of Secrets",
    "author_id": 1,
    "description": "The second book in the series",
    "isbn": "9780439064873",
    "publication_date": "1998-07-02",
    "pages": 251,
    "price": "14.99",
    "in_stock": true
  }'
```

**Response (201 Created):**

```json
{
  "id": 2,
  "title": "Harry Potter and the Chamber of Secrets",
  ...
}
```

#### Get Book Detail

**GET** `/api/books/{id}/`

Public endpoint.

**Response (200 OK):**

```json
{
  "id": 1,
  "title": "Harry Potter and the Philosopher's Stone",
  ...
}
```

#### Update Book

**PUT** `/api/books/{id}/`

Requires authentication.

**Request:**

```bash
curl -X PUT http://localhost:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "rating": 4.8,
    "price": "16.99"
  }'
```

#### Delete Book

**DELETE** `/api/books/{id}/`

Requires authentication.

**Response:** 204 No Content

#### Set Book Rating

**POST** `/api/books/{id}/set_rating/`

Custom action to rate a book.

**Request:**

```bash
curl -X POST http://localhost:8000/api/books/1/set_rating/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "rating": 4.5
  }'
```

**Response (200 OK):**

```json
{
  "id": 1,
  "rating": 4.5,
  ...
}
```

#### Toggle Book Stock

**POST** `/api/books/{id}/toggle_stock/`

Custom action to toggle stock availability.

**Request:**

```bash
curl -X POST http://localhost:8000/api/books/1/toggle_stock/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response (200 OK):**

```json
{
  "id": 1,
  "in_stock": false,
  ...
}
```

#### Get Top-Rated Books

**GET** `/api/books/top_rated/`

Public endpoint - returns top-rated books.

**Query Parameters:**

- `limit`: Number of books to return (default: 5)

**Example:**

```bash
curl "http://localhost:8000/api/books/top_rated/?limit=10"
```

**Response (200 OK):**

```json
[
  {
    "id": 5,
    "title": "The Great Gatsby",
    "rating": 5.0,
    ...
  }
]
```

#### Get Available Books

**GET** `/api/books/available/`

Public endpoint - returns books in stock.

**Response (200 OK):**

```json
[
  {
    "id": 1,
    "title": "Harry Potter and the Philosopher's Stone",
    "in_stock": true,
    ...
  }
]
```

---

### Users Endpoints

#### Register User

**POST** `/api/users/`

Public endpoint - no authentication required.

**Request:**

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "new_user",
    "email": "newuser@example.com",
    "password": "secure_password_123"
  }'
```

**Response (201 Created):**

```json
{
  "id": 1,
  "username": "new_user",
  "email": "newuser@example.com",
  "first_name": "",
  "last_name": "",
  "is_active": true,
  "is_staff": false
}
```

#### Get Current User Profile

**GET** `/api/users/me/`

Requires authentication - returns the authenticated user's profile.

**Response (200 OK):**

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "is_staff": false
}
```

#### Get User Detail

**GET** `/api/users/{id}/`

Requires authentication.

**Response (200 OK):**

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "is_staff": false
}
```

#### Update User

**PUT** `/api/users/{id}/`

Requires authentication.

**Request:**

```bash
curl -X PUT http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "first_name": "Jonathan",
    "last_name": "Doe"
  }'
```

---

## Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "detail": "Error message here"
}
```

Or for validation errors:

```json
{
  "field_name": ["Error message"],
  "another_field": ["Error message 1", "Error message 2"]
}
```

### Common HTTP Status Codes

| Status | Meaning                                 |
| ------ | --------------------------------------- |
| 200    | OK - Request successful                 |
| 201    | Created - Resource created successfully |
| 204    | No Content - Successful deletion        |
| 400    | Bad Request - Invalid input data        |
| 401    | Unauthorized - Authentication required  |
| 403    | Forbidden - Permission denied           |
| 404    | Not Found - Resource not found          |
| 500    | Server Error - Internal server error    |

### Example Error Responses

**401 Unauthorized:**

```json
{
  "detail": "Authentication credentials were not provided."
}
```

**404 Not Found:**

```json
{
  "detail": "Not found."
}
```

**400 Bad Request:**

```json
{
  "title": ["This field may not be blank."],
  "isbn": ["This field must be unique."]
}
```

---

## Rate Limiting & Pagination

### Pagination

Results are paginated by default with 10 items per page.

**Query Parameters:**

- `page`: Page number (default: 1)

**Response includes:**

- `count`: Total number of items
- `next`: URL to next page
- `previous`: URL to previous page
- `results`: Array of items

**Example:**

```bash
curl "http://localhost:8000/api/books/?page=2"
```

---

## Field Validation

### Author Fields

| Field      | Type   | Required | Notes              |
| ---------- | ------ | -------- | ------------------ |
| name       | string | Yes      | Max 255 characters |
| email      | string | Yes      | Must be unique     |
| bio        | string | No       | Unlimited text     |
| birth_date | date   | No       | Format: YYYY-MM-DD |

### Book Fields

| Field            | Type    | Required | Notes                     |
| ---------------- | ------- | -------- | ------------------------- |
| title            | string  | Yes      | Max 255 characters        |
| author_id        | integer | Yes      | Must be valid author ID   |
| description      | string  | Yes      | Unlimited text            |
| isbn             | string  | Yes      | Max 13 characters, unique |
| publication_date | date    | Yes      | Format: YYYY-MM-DD        |
| pages            | integer | Yes      | Must be > 0               |
| rating           | float   | No       | 0-5, default: 0           |
| price            | decimal | Yes      | Format: 0.00              |
| in_stock         | boolean | No       | Default: true             |

---

## Best Practices

1. **Always include Content-Type header** for POST/PUT requests
2. **Use pagination** when fetching large datasets
3. **Cache access tokens** to reduce API calls
4. **Handle refresh tokens** before they expire
5. **Validate input data** on the client side
6. **Use query parameters** for filtering instead of retrieving all data
7. **Implement proper error handling** in your client application

---

## Examples Using Different Tools

### Using Postman

1. Create new request
2. Set method to POST
3. Set URL to `http://localhost:8000/api/token/`
4. Go to Body tab, select JSON
5. Enter credentials:
   ```json
   {
     "username": "john_doe",
     "password": "password"
   }
   ```
6. Send and copy the access token
7. For authenticated requests, go to Headers and add:
   - Key: `Authorization`
   - Value: `Bearer YOUR_ACCESS_TOKEN`

### Using Python (requests library)

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Get token
response = requests.post(f"{BASE_URL}/token/", json={
    "username": "john_doe",
    "password": "password"
})
token = response.json()["access"]

# Get books
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/books/", headers=headers)
books = response.json()
print(books)
```

### Using JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000/api";

async function getBooks() {
  const tokenResponse = await fetch(`${BASE_URL}/token/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: "john_doe",
      password: "password",
    }),
  });

  const { access } = await tokenResponse.json();

  const response = await fetch(`${BASE_URL}/books/`, {
    headers: { Authorization: `Bearer ${access}` },
  });

  const books = await response.json();
  console.log(books);
}

getBooks();
```

---

## Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

**Repository:** https://github.com/MadhuKosuri1/Build-a-REST-API
