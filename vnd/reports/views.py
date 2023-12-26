from django.views.generic import DetailView, ListView

from reports.models import Report


class ReportDetailView(DetailView):
    template_name = "admin/reports/report/report_detail.html"
    model = Report


class ReportListView(ListView):
    template_name = "admin/reports/report/change_form.html"
    model = Report


