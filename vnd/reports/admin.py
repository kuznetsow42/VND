import datetime

from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.html import format_html
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import action

from posts.models import Post
from reports.models import Report, Reason, ClosedReport, Ban


@admin.register(Report)
class ReportAdmin(ModelAdmin):
    list_display = ["id", "reported_at", "reason", "closed", "content_instance"]
    list_display_links = list_display
    list_filter = ["closed", "reason", "reason__top_priority"]
    actions_detail = ["approve"]

    def content(self, obj):
        reported_content = obj.content_instance
        if isinstance(reported_content, Post):
            return format_html(reported_content.body)
        return reported_content.text

    @action(description="Approve report")
    def approve(self, request: HttpRequest, object_id: int):
        report = Report.objects.get(pk=object_id)
        closed_report = report.close(approved=True, admin=request.user)
        report.closed = True
        report.save()
        if report.reason.top_priority:
            user = report.reported_user
            if hasattr(user, 'bans'):
                user.is_active = False
            else:
                ban_end = datetime.date.today() + datetime.timedelta(days=31)
                report.content_instance.delete()
                Ban.objects.create(reason=closed_report, user=user, end=ban_end)
        return redirect(f"/admin/reports/")


@admin.register(ClosedReport)
class ClosedReportAdmin(ModelAdmin):
    list_display = ["id", "timestamp", "closed_by"]
    list_display_links = list_display
    list_filter = ["objected"]
    readonly_fields = ["timestamp", "closed_by", "report", "objected", "approved"]


admin.site.register(Reason)
admin.site.register(Ban)
