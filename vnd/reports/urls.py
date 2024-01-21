from django.urls import path

from .views import ReasonsListView, ReportView

urlpatterns = [
    path('reasons/', ReasonsListView.as_view()),
    path('', ReportView.as_view()),
]
