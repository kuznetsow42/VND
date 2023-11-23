from rest_framework import serializers

from api.models import Tag
from api.sanitizer import sanitize_text
from posts.models import Image, Post, UserPostRelation, Category
from users.serializers import UserSerializer


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


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def validate_body(self, value):
        clear_body = sanitize_text(value)
        return clear_body


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(read_only=True)
    relation = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    authors = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "body", "tags", "created_at", "likes", "relation", "readers", "categories", "authors"]

    def get_relation(self, obj):
        user = self.context["request"].user
        if user.is_anonymous or user not in obj.readers.all():
            return {
                "like": False,
                "bookmark": False
            }
        relation = UserPostRelation.objects.get(user=user.pk, post=obj.pk)
        return {
            "like": relation.like,
            "bookmark": relation.bookmark
        }


class UserPostRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPostRelation
        fields = ["user", "post", "like", "bookmark"]

    def update_or_create(self):
        user = self.validated_data.get("user")
        post = self.validated_data.get("post")
        instance, created = UserPostRelation.objects.update_or_create(user=user, post=post,
                                                                      defaults=self.validated_data)
        return self.to_representation(instance), created
