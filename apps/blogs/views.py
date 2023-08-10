from rest_framework import exceptions, mixins, permissions, response, status, viewsets
from rest_framework.decorators import action

from apps.blogs.models import Blog, Post
from apps.blogs.serializers import (
    BlogSeriazlier,
    PostReadSerializer,
    PostWriteSeriazliser,
)
from apps.blogs.utils import get_posts_for_user_feed


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
        user.seen_posts.add(post)
        return response.Response({"seen": "OK"}, status=status.HTTP_201_CREATED)


class BlogViewSet(viewsets.GenericViewSet):
    queryset = Blog.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["POST"], url_path="follow")
    def follow_blog(self, request, pk=None):
        user = self.request.user
        blog = self.get_object()
        if user == blog.owner:
            raise exceptions.ValidationError("Вы не можете подписаться на себя")  # TODO: exceptions
        if blog in user.follows.all():
            raise exceptions.ValidationError("Вы уже подписаны на этот блог")
        user.follows.add(blog)
        serializer = BlogSeriazlier(instance=blog)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"], url_path="unfollow")
    def unfollow_blog(self, request, pk=None):
        user = self.request.user
        blog = self.get_object()
        if blog not in user.follows.all():
            raise exceptions.ValidationError("Вы не подписаны на этот блог")
        user.follows.remove(blog)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class FeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostReadSerializer

    def get_queryset(self):  # TODO: add filters
        return get_posts_for_user_feed(self.request.user, 500)  # TODO: add constants
