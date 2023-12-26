from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.html import format_html
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import action

from posts.models import Post
from reports.models import Report, Reason


@admin.register(Report)
class ReportAdmin(ModelAdmin):
    list_display = ["id", "reported_at", "reason", "approved", "content_instance"]
    list_display_links = list_display
    list_filter = ["approved", "reason", "reason__top_priority"]
    readonly_fields = ["reason", "reporting_user", "content_instance", "content", "content_model", "content_id"]
    actions_detail = ["remove_content"]

    def content(self, obj):
        reported_content = obj.content_instance
        if isinstance(reported_content, Post):
            return format_html(reported_content.body)
        return reported_content.text

    @action(description="Remove content")
    def remove_content(self, request: HttpRequest, object_id: int):
        report = Report.objects.get(pk=object_id)
        report.approved = True
        report.save()
        report.content_instance.delete()
        return redirect(f"/admin/reports/")


admin.site.register(Reason)
