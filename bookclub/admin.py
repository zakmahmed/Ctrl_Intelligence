from django.contrib import admin
from .models import User, Club, Book, Application , Post
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email', 'location', 'age', 'is_active',
    ]


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'location', 'description'
    ]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'isbn', 'title', 'author', 'pub_year'
    ]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'applicant', 'club'
    ]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for posts."""

    list_display = [
        'get_author', 'text', 'created_at',
    ]

    def get_author(self, post):
        """Return the author of a given post."""
        return post.author.username