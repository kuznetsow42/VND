from django.urls import path

from comments.views import ChangeRelation

urlpatterns = [
    path("post_comments/<int:pk>/", ChangeRelation.as_view())
]
