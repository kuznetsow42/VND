from rest_framework import serializers

from api.models import Tag
from api.sanitizer import sanitize_text
from posts.models import Image, Post, Category
from api.utils import get_user_relations
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
    relation = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField()
    bookmarks_count = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ["id", "title", "body", "tags", "created_at", "categories", "authors",
                  "relation", "likes_count", "bookmarks_count"]
        depth = 1

    def get_relation(self, obj):
        return get_user_relations(self.context["request"], obj)
