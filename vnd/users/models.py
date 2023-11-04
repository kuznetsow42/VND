from django.contrib.auth.models import AbstractUser
from django.db import models


class Engine(models.Model):
    name = models.CharField(max_length=70)
    image = models.ImageField(upload_to="engines", default="engines/default.png")
    links = models.JSONField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Statuses"


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="users/avatars", default="users/avatars/default.png", blank=True)
    status = models.ForeignKey(Status, related_name="users", to_field="name",
                               on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    favorite_engines = models.ManyToManyField(Engine, related_name="users", blank=True)
    links = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.username
