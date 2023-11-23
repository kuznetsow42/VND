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
    readers = models.ManyToManyField(CustomUser, through="UserPostRelation", related_name="post_relations")

    def __str__(self):
        return self.title


class Image(models.Model):
    file = models.ImageField(upload_to="posts/images")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)


class UserPostRelation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    bookmark = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} -- {self.post}"
