from rest_framework import serializers

from apps.blogs.models import Blog, Post


class PostReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "text", "created_at", "blog"]


class PostWriteSeriazliser(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "text"]


class BlogSeriazlier(serializers.ModelSerializer):  # TODO: поменять модель
    class Meta:
        model = Blog
        fields = ["id"]
