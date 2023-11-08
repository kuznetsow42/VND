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
