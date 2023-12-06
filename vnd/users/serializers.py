from rest_framework import serializers
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin

from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.serializers import EngineSerializer
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
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["avatar"] = user.avatar.url
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar", "status", "bio", "favorite_engines", "links", "first_name", "last_name"]
        depth = 1


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
