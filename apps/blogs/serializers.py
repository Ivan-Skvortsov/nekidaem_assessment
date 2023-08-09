from rest_framework import serializers

from apps.blogs.models import Blog, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "text", "created_at", "blog"]


class BlogSeriazlier(serializers.ModelSerializer):
    class Meta:
        models = Blog
        fields = "__all__"  # TODO
