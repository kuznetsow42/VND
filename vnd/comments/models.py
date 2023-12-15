from django.db import models

from users.models import CustomUser


class CommentBaseModel(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="comments")
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="comments", blank=True)
    text = models.TextField()
    likes = models.ManyToManyField(CustomUser, related_name="liked_comments", blank=True)
    bookmarks = models.ManyToManyField(CustomUser, related_name="bookmarked_comments", blank=True)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, related_name="children")

    def __str__(self):
        return self.text

    class Meta:
        abstract = True
