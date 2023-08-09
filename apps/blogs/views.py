from django.db import IntegrityError
from rest_framework import exceptions, mixins, permissions, response, status, viewsets
from rest_framework.decorators import action

from apps.blogs.models import Blog, Post
from apps.blogs.serializers import (
    BlogSeriazlier,
    PostReadSerializer,
    PostWriteSeriazliser,
)
from apps.users.models import SeenPosts


class PostViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return PostReadSerializer
        return PostWriteSeriazliser

    def perform_create(self, serializer):
        serializer.save(blog=self.request.user.blog)

    @action(detail=True, methods=["POST"], url_path="seen")
    def mark_post_as_seen(self, request, pk=None):
        post = self.get_object()
        user = self.request.user
        try:
            SeenPosts.objects.create(user=user, post=post)
            return response.Response({"seen": "OK"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            raise exceptions.NotAcceptable("Пользователь уже пометил пост прочитанным")  # TODO


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSeriazlier
