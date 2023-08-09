from rest_framework import viewsets

from apps.blogs.models import Blog, Post
from apps.blogs.serializers import BlogSeriazlier, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSeriazlier
