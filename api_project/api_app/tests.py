"""
Tests for the API app.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api_project.api_app.models import Author, Book
from datetime import date


class AuthorTestCase(APITestCase):
    """Test cases for Author model and viewset."""

    def setUp(self):
        """Set up test client and create test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(
            name='John Doe',
            email='john@example.com',
            bio='Test author',
            birth_date='1980-01-01'
        )

    def test_list_authors(self):
        """Test listing all authors."""
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_create_author_authenticated(self):
        """Test creating an author when authenticated."""
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'bio': 'Another test author'
        }
        response = self.client.post('/api/authors/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_author_unauthenticated(self):
        """Test that unauthenticated users cannot create authors."""
        data = {
            'name': 'Jane Smith',
            'email': 'jane@example.com'
        }
        response = self.client.post('/api/authors/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_author(self):
        """Test retrieving a specific author."""
        response = self.client.get(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')


class BookTestCase(APITestCase):
    """Test cases for Book model and viewset."""

    def setUp(self):
        """Set up test client and create test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(
            name='Test Author',
            email='author@example.com'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            description='A test book',
            isbn='1234567890123',
            publication_date='2023-01-01',
            pages=300,
            price=19.99,
            created_by=self.user
        )

    def test_list_books(self):
        """Test listing all books."""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_authenticated(self):
        """Test creating a book when authenticated."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Book',
            'author_id': self.author.id,
            'description': 'A new book',
            'isbn': '1234567890124',
            'publication_date': '2023-06-01',
            'pages': 250,
            'price': 24.99
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        data = {
            'title': 'New Book',
            'author_id': self.author.id,
            'description': 'A new book',
            'isbn': '1234567890124',
            'publication_date': '2023-06-01',
            'pages': 250,
            'price': 24.99
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_set_book_rating(self):
        """Test setting a book rating."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/books/{self.book.id}/set_rating/', {'rating': 4.5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['rating']), 4.5)

    def test_toggle_stock(self):
        """Test toggling book stock status."""
        self.client.force_authenticate(user=self.user)
        initial_status = self.book.in_stock
        response = self.client.post(f'/api/books/{self.book.id}/toggle_stock/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['in_stock'], not initial_status)

    def test_top_rated_books(self):
        """Test getting top-rated books."""
        response = self.client.get('/api/books/top_rated/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_available_books(self):
        """Test getting available books."""
        response = self.client.get('/api/books/available/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
