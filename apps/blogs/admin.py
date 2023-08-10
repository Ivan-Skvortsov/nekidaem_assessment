from django.contrib import admin

from apps.blogs.models import Blog, Post
from apps.users.models import User


class UserInLine(admin.StackedInline):
    model = User


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    model = Blog
    inlines = [UserInLine]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ["id", "title", "text", "author_username"]
    fields = ["title", "text"]

    @admin.display(description="Автор")
    def author_username(self, obj):
        return obj.blog.owner.username
