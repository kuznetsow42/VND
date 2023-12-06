from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import Engine, Status
from .serializers import EngineSerializer, StatusSerializer


class EngineViewSet(ModelViewSet):
    pagination_class = None
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]


class StatusViewSet(ModelViewSet):
    pagination_class = None
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

