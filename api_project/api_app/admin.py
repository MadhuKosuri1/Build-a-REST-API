from django.contrib import admin
from api_project.api_app.models import Book, Author

# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'birth_date', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Author Information', {
            'fields': ('name', 'email', 'bio', 'birth_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'rating', 'price', 'in_stock', 'created_at']
    list_filter = ['author', 'in_stock', 'rating', 'created_at']
    search_fields = ['title', 'isbn', 'author__name']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'description', 'isbn')
        }),
        ('Publication Details', {
            'fields': ('publication_date', 'pages')
        }),
        ('Availability', {
            'fields': ('in_stock', 'rating', 'price')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
