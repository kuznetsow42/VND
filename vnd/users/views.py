from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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

    def patch(self, request, *args, **kwargs):
        data = request.data
        if "favorite_engines" not in data:
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            user = self.get_object()
            serializer = self.get_serializer(user, data=data, partial=True)
            if data["action"] == "delete":
                user.favorite_engines.remove(data["favorite_engines"])
            else:
                user.favorite_engines.add(data["favorite_engines"])
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)


