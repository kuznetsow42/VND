from rest_framework import serializers

from api.models import Tag
from api.sanitizer import sanitize_text
from posts.models import Image, Post, Category
from users.models import CustomUser


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar", "status", "bio", "links", "first_name", "last_name"]


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "id", "body", "tags", "categories", "authors"]

    def validate_body(self, value):
        clear_body = sanitize_text(value)
        return clear_body


class PostSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()
    bookmarks = serializers.SerializerMethodField()
    relation = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "body", "tags", "created_at", "likes", "categories", "authors", "bookmarks",
                  "relation"]
        depth = 1

    def get_likes(self, obj):
        return obj.likes.count()

    def get_bookmarks(self, obj):
        return obj.bookmarks.count()

    def get_relation(self, obj):
        user = self.context["request"].user
        user_relation = {"like": False, "bookmark": False}
        if user.is_anonymous:
            return user_relation
        user_relation["like"] = user in obj.likes.all()
        user_relation["bookmark"] = user in obj.bookmarks.all()
        return user_relation
