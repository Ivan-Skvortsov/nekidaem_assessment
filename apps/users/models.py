from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.blogs.models import Blog, Post


class User(AbstractUser):
    blog = models.OneToOneField(Blog, related_name="owner", on_delete=models.CASCADE, verbose_name="Блог пользователя")
    follows = models.ManyToManyField(Blog, related_name="followed_by", blank=True, verbose_name="Подписки пользователя")
    seen_posts = models.ManyToManyField(Post, related_name="seen_by", blank=True, verbose_name="Просмотренные посты")

    def save(self, *args, **kwargs):
        self.blog = Blog.objects.create()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.blog.delete()
        super().delete(*args, **kwargs)
