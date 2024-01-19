from django.contrib.auth import get_user
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
    closed = models.BooleanField(default=False)
    reporting_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="reports", null=True)
    reported_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content_model.name} : {str(self.content_instance)}"

    def close(self, approved: bool, admin: CustomUser):
        self.closed = True
        closed_report = ClosedReport.objects.create(report=self, closed_by=admin, approved=approved)
        return closed_report


class ClosedReport(models.Model):
    closed_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="closed_reports")
    timestamp = models.DateTimeField(auto_now_add=True)
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    approved = models.BooleanField()
    objected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.closed_by} | {self.report}"


class Ban(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="bans")
    reason = models.ForeignKey(ClosedReport, on_delete=models.CASCADE)
    end = models.DateTimeField()

    def __str__(self):
        return f"{self.user} | {self.reason.report.reason}"
