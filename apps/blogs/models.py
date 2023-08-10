from django.db import models


class Blog(models.Model):
    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"


class Post(models.Model):
    title = models.CharField(max_length=140, blank=False, verbose_name="Заголовок поста")
    text = models.TextField(verbose_name="Текст поста")
    created_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="posts", verbose_name="Блог")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return f"Пост {self.title}"
