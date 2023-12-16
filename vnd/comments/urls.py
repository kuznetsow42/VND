from django.urls import path

from comments.views import ChangePostCommentsRelation

urlpatterns = [
    path("post_comments/<int:pk>/", ChangePostCommentsRelation.as_view())
]
