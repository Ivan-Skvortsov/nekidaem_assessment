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


class BlogSeriazlier(serializers.ModelSerializer):
    class Meta:
        models = Blog
        fields = "__all__"  # TODO
