from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.models import CustomUser
from users.serializers import RegisterSerializer, UserSerializer, UserDetailSerializer


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



