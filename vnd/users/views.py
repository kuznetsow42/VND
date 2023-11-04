from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from users.models import CustomUser, Engine, Status
from users.serializers import RegisterSerializer, UserSerializer, UserDetailSerializer, EngineSerializer, \
    StatusSerializer


class Register(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class UsersReadOnly(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.pk)


class EngineViewSet(ModelViewSet):
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]
