from rest_framework import serializers

from posts.models import PostComment
from api.utils import get_user_relations
from users.serializers import LightUserSerializer


class CreatePostCommentSerializer(serializers.ModelSerializer):
    author = LightUserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = "__all__"
        extra_kwargs = {"author": {"required": False}, "post": {"required": False}}


class PostCommentSerializer(serializers.ModelSerializer):
    author = LightUserSerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    relation = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ["id", "author", "image", "text", "created_at", "likes_count", "bookmarks_count", "relation",
                  "replies_count"]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_bookmarks_count(self, obj):
        return obj.bookmarks.count()

    def get_replies_count(self, obj):
        return obj.children.count()

    def get_relation(self, obj):
        return get_user_relations(self.context["request"], obj)
        
