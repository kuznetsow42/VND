from django.utils import timezone
from rest_framework import serializers
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin

from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser

from api.serializers import EngineSerializer
from reports.serializers import BanSerializer
from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar", "status", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs["password"]
        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password is too short."})
        attrs["password"] = make_password(password)
        return attrs


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser):
        if hasattr(user, 'bans'):
            ban = user.bans
            ban_end_time = ban.end
            remaining_time = ban_end_time - timezone.now()
            if remaining_time.seconds > 0:
                raise exceptions.AuthenticationFailed(f"This account baned for {remaining_time.days} days and "
                                                      f"{remaining_time.seconds // 3600} hours")
        token = super().get_token(user)
        token["username"] = user.username
        token["avatar"] = user.avatar.url
        token["id"] = user.id
        return token


class LightUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar"]


class UserSerializer(serializers.ModelSerializer):
    relations = serializers.SerializerMethodField()
    subscribers_count = serializers.IntegerField()
    posts_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar", "status", "bio", "favorite_engines", "links", "first_name", "last_name",
                  "relations", "subscribers_count", "posts_count"]
        depth = 1

    def get_relations(self, obj):
        user = self.context["request"].user
        user_relation = {"subscribed": False}
        if user.is_anonymous:
            return user_relation
        user_relation["subscribed"] = user in obj.subscribers.all()
        return user_relation


class UserDetailSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar", "email", "bio", "links", "first_name", "last_name", "status"]
        expandable_fields = {
            "favorite_engines": {
                "serializer": EngineSerializer,
                "many": True,
                "readonly": False
            }
        }
