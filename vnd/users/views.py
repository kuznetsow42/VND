from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin

from users.models import CustomUser
from users.serializers import RegisterSerializer, UserSerializer, UserDetailSerializer


class Register(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class UsersReadOnly(ReadOnlyModelViewSet):
    ordering_fields = ["username"]
    filterset_fields = ["status", "favorite_engines", "subscribers"]
    queryset = CustomUser.objects.select_related("status") \
        .prefetch_related("favorite_engines", "subscribers") \
        .annotate(subscribers_count=Count("subscribers", distinct=True), posts_count=Count("posts", distinct=True))
    serializer_class = UserSerializer

    @action(detail=True, methods=["patch", "delete"], permission_classes=[IsAuthenticated])
    def subscriptions(self, request, pk):
        if request.method == "PATCH":
            request.user.subscriptions.add(pk)
        else:
            request.user.subscriptions.remove(pk)
        serializer = self.serializer_class(self.get_object(), context={"request": request})
        return Response(serializer.data, 200)


class UserDetail(SerializerExtensionsAPIViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    extensions_expand = {'favorite_engines'}

    def get_object(self):
        return CustomUser.objects.select_related("status").get(pk=self.request.user.pk)

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
