from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.blogs.models import Blog


class User(AbstractUser):
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE, verbose_name="Блог пользователя")
    follows = models.ManyToManyField(Blog, related_name="followed_by", blank=True, verbose_name="Подписки пользователя")

    def save(self, *args, **kwargs):
        blog = Blog.objects.create()
        self.blog = blog
        super().save(*args, **kwargs)
