"""
Serializers for the API app.
Serializes Book and Author models to/from JSON.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from api_project.api_app.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author model."""
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio', 'birth_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model with author details."""
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'author_id',
            'description',
            'isbn',
            'publication_date',
            'pages',
            'rating',
            'price',
            'in_stock',
            'created_by',
            'created_by_username',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Create a book and set the creator as the current user.
        """
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new user with hashed password."""
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
