from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200, default="Название вашего блога", verbose_name="Название блога")
    description = models.TextField(max_length=2000, default="Описание вашего блога", verbose_name="Описание блога")

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"

    def __str__(self):
        return f"Блог: {self.title[:50]}"


class Post(models.Model):
    title = models.CharField(max_length=140, blank=False, verbose_name="Заголовок поста")
    text = models.TextField(verbose_name="Текст поста")
    created_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="posts", verbose_name="Блог")

    class Meta:
        order_by = ["-created_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return f"Пост {self.title}"
