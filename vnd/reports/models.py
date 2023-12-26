from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from users.models import CustomUser


class Reason(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200, blank=True, null=True)
    top_priority = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Report(models.Model):
    content_model = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content_instance = GenericForeignKey("content_model", "content_id")
    reported_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    reporting_user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="reports")
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content_model.name} : {self.content_instance.__str__()}"
