from django.db.models import Count, Q
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from api.models import Tag
from api.permissions import IsOwnerOrAdmin
from posts.models import Image, Post, Category
from posts.serializers import ImageSerializer, PostSerializer, UserPostRelationSerializer, CategorySerializer, \
    TagSerializer, CreatePostSerializer


class AddImage(ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().annotate(likes=Count("userpostrelation", filter=Q(userpostrelation__like=True)))
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        return [AllowAny()]

    def get_serializer(self, *args, **kwargs):
        if self.action in ["list", "retrieve"]:
            return PostSerializer(*args, **kwargs, context={"request": self.request})
        return CreatePostSerializer(*args, **kwargs)

    @action(detail=True, methods=["post", "patch"])
    def set_relation(self, request, pk):
        data = request.data
        data["user"] = request.user.pk
        data["post"] = pk
        serializer = UserPostRelationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance, created = serializer.update_or_create()
        if created:
            status_code = HTTP_201_CREATED
        else:
            status_code = HTTP_200_OK
        return Response(instance, status=status_code)
