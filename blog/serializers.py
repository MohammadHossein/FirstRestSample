from rest_framework import serializers

from blog.models import Post, Comment
from .models import MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'password')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('commentId', 'user', 'text', 'date', 'post')


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True)

    # comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ('postId', 'user', 'text', 'date', 'comments')
