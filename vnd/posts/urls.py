from django.urls import path
from rest_framework.routers import SimpleRouter

from posts.views import AddImage, PostViewSet, CategoryViewSet, TagViewSet

router = SimpleRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"tags", TagViewSet)
router.register(r"", PostViewSet)


urlpatterns = [
    path("add_image/", AddImage.as_view()),
] + router.urls
