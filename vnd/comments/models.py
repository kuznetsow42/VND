from django.db import models

from users.models import CustomUser


class CommentBaseModel(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="comments", null=True)
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="comments", blank=True)
    text = models.TextField()
    likes = models.ManyToManyField(CustomUser, related_name="liked_comments", blank=True)
    bookmarks = models.ManyToManyField(CustomUser, related_name="bookmarked_comments", blank=True)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, related_name="children")

    def __str__(self):
        return self.text

    def delete(self, using=None, keep_parents=False):
        self.image = None
        self.text = "Removed by moderator"
        self.save()

    def get_owner(self):
        return self.author.pk

    class Meta:
        abstract = True
