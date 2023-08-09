from rest_framework import serializers

from apps.blogs.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "text", "created_at", "blog"]
