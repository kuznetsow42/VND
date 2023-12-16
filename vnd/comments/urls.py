from django.urls import path

from comments.views import ChangePostCommentsRelation, BookmarkedCommentsList

urlpatterns = [
    path("post_comments/<int:pk>/", ChangePostCommentsRelation.as_view()),
    path("bookmarks/", BookmarkedCommentsList.as_view()),
]
