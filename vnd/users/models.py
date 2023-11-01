from django.contrib.auth.models import AbstractUser
from django.db import models


class Link(models.Model):
    name = models.CharField(max_length=70)
    url = models.URLField()
    type = models.CharField(choices=[
        ("d", "Documentation"),
        ("w", "WebSite"),
        ("s", "Social media"),
        ("c", "Code"),
    ])
    icon = models.ImageField(upload_to="icons")

    def __str__(self):
        return self.name


class Engine(models.Model):
    name = models.CharField(max_length=70)
    links = models.ManyToManyField(Link)
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
    avatar = models.ImageField(upload_to="users/avatars")
    status = models.ForeignKey(Status, related_name="users", to_field="name",
                               on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField()
    favorite_engines = models.ManyToManyField(Engine, related_name="users")
    links = models.ManyToManyField(Link)

    def __str__(self):
        return self.username
