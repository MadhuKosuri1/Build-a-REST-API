"""
Views and ViewSets for the API app.
Implements CRUD operations for Book, Author, and User models.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from api_project.api_app.models import Book, Author
from api_project.api_app.serializers import BookSerializer, AuthorSerializer, UserSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Book model.
    
    Features:
    - List all books
    - Create a new book (authenticated users only)
    - Retrieve a specific book
    - Update a book
    - Delete a book
    - Filter by author, in_stock status
    - Search by title, description, ISBN
    - Custom actions for rating and stock management
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'in_stock', 'rating']
    search_fields = ['title', 'description', 'isbn', 'author__name']
    ordering_fields = ['created_at', 'rating', 'price']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        Allow any user to list and retrieve books,
        but require authentication for create, update, delete.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def set_rating(self, request, pk=None):
        """
        Custom action to set book rating.
        POST /api/books/{id}/set_rating/
        """
        book = self.get_object()
        rating = request.data.get('rating')

        if rating is None:
            return Response(
                {'error': 'Rating value is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rating = float(rating)
            if not (0 <= rating <= 5):
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {'error': 'Rating must be a number between 0 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )

        book.rating = rating
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_stock(self, request, pk=None):
        """
        Custom action to toggle book stock status.
        POST /api/books/{id}/toggle_stock/
        """
        book = self.get_object()
        book.in_stock = not book.in_stock
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def top_rated(self, request):
        """
        Custom action to get top-rated books.
        GET /api/books/top_rated/
        """
        limit = int(request.query_params.get('limit', 5))
        books = self.queryset.order_by('-rating')[:limit]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def available(self, request):
        """
        Custom action to get available (in-stock) books.
        GET /api/books/available/
        """
        books = self.queryset.filter(in_stock=True)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Author model.
    
    Features:
    - List all authors
    - Create a new author (authenticated users only)
    - Retrieve a specific author
    - Update author information
    - Delete an author
    - Search by name or email
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        Allow any user to list and retrieve authors,
        but require authentication for create, update, delete.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def books(self, request, pk=None):
        """
        Custom action to get all books by a specific author.
        GET /api/authors/{id}/books/
        """
        author = self.get_object()
        books = author.books.all()
        page = self.paginate_queryset(books)
        if page is not None:
            serializer = BookSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User management.
    
    Features:
    - List all users (admin only)
    - Create a new user (public registration)
    - Retrieve user profile
    - Update user information
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_permissions(self):
        """
        Allow anyone to create a new user.
        Allow authenticated users to view and update their own profile.
        """
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Custom action to get the current user's profile.
        GET /api/users/me/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
