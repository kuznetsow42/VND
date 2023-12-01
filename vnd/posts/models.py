from django.db import models

from api.models import Tag
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(CustomUser, related_name="posts")
    categories = models.ManyToManyField(Category, related_name="posts",)
    tags = models.ManyToManyField(Tag, related_name="posts")
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name="liked_posts", blank=True)
    bookmarks = models.ManyToManyField(CustomUser, related_name="bookmarked_posts", blank=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    file = models.ImageField(upload_to="posts/images")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
