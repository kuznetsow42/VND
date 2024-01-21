from django.contrib.auth.models import AbstractUser
from django.db import models

from api.models import Status, Engine


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="users/avatars", default="users/avatars/default.png", blank=True)
    status = models.ForeignKey(Status, related_name="users", to_field="name",
                               on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    favorite_engines = models.ManyToManyField(Engine, related_name="users", blank=True)
    links = models.JSONField(blank=True, null=True)
    subscriptions = models.ManyToManyField("self", blank=True, related_name="subscribers", symmetrical=False)

    def __str__(self):
        return self.username

    def get_owner(self):
        return self
