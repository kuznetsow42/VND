from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.serializers import CommentSerializer
from posts.models import PostComment


class ChangePostCommentsRelation(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        comment = PostComment.objects.get(pk=pk)
        if "like" in request.data:
            if request.data["like"]:
                comment.likes.add(request.user)
            else:
                comment.likes.remove(request.user)
        if "bookmark" in request.data:
            if request.data["bookmark"]:
                comment.bookmarks.add(request.user)
            else:
                comment.bookmarks.remove(request.user)
        comment.save()
        return Response(CommentSerializer(comment, context={"request": request}).get_relation(comment), 200)


class BookmarkedCommentsList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.request.user.bookmarked_comments.all()

