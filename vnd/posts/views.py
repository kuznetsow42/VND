from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from api.models import Tag
from api.permissions import IsOwnerOrAdmin
from posts.models import Image, Post, Category
from posts.serializers import ImageSerializer, PostSerializer, CategorySerializer, \
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
    queryset = Post.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["tags", "categories", "authors"]
    ordering_fields = ["likes", "title", "bookmarks"]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer(self, *args, **kwargs):
        if self.action in ["list", "retrieve"]:
            return PostSerializer(*args, **kwargs, context={"request": self.request})
        return CreatePostSerializer(*args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.prefetch_related(
            "authors",
            "authors__status",
            "tags",
            "categories",
            "likes",
            "bookmarks"
        )
        return queryset

    @action(detail=True, methods=["post"])
    def set_relation(self, request, pk):
        post = Post.objects.get(pk=pk)
        if "like" in request.data:
            if request.data["like"]:
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)
        if "bookmark" in request.data:
            if request.data["bookmark"]:
                post.bookmarks.add(request.user)
            else:
                post.bookmarks.remove(request.user)
        post.save()
        return Response(PostSerializer(post, context={"request": request}).get_relation(post),
                        status=HTTP_200_OK)
