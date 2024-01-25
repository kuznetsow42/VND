from django.urls import path

from .views import ReasonsListView, ReportView, ClosedReportsView, OpenedReportsView

urlpatterns = [
    path('reasons/', ReasonsListView.as_view()),
    path('opened/', OpenedReportsView.as_view()),
    path('closed/', ClosedReportsView.as_view()),
    path('', ReportView.as_view()),
]
