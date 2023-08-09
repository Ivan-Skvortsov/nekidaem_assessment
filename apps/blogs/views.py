from rest_framework import viewsets

from apps.blogs.models import Post
from apps.blogs.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
