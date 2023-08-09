from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.blogs.models import Blog, Post


class User(AbstractUser):
    blog = models.OneToOneField(Blog, related_name="owner", on_delete=models.CASCADE, verbose_name="Блог пользователя")
    follows = models.ManyToManyField(Blog, related_name="followed_by", blank=True, verbose_name="Подписки пользователя")

    def save(self, *args, **kwargs):
        self.blog = Blog.objects.create()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.blog.delete()
        super().delete(*args, **kwargs)


class SeenPosts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "post"], name="unique_seen_post_entry")]

    def __str__(self):
        return f"Просмотр поста {self.post} пользователем {self.user}"
