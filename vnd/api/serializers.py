from rest_framework import serializers


from .models import Engine, Status


class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engine
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"
