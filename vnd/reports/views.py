from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from reports.models import Reason, Report, ClosedReport
from reports.serializers import ReasonSerializer, ReportSerializer, CreateReportSerializer, ClosedReportsSerializer
from reports.utils import get_model_object


class ReasonsListView(ListAPIView):
    serializer_class = ReasonSerializer
    queryset = Reason.objects.all()
    pagination_class = None


class OpenedReportsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer
    pagination_class = None

    def get_queryset(self):
        return Report.objects.filter(closed=False, reporting_user=self.request.user)


class ClosedReportsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClosedReportsSerializer
    pagination_class = None

    def get_queryset(self):
        return ClosedReport.objects.filter(report__reporting_user=self.request.user)


class ReportView(CreateAPIView):
    serializer_class = CreateReportSerializer

    def create(self, request, *args, **kwargs):
        user = None
        if request.user.is_authenticated:
            user = request.user
        data = request.data
        model = get_model_object(data["model"])
        instance = model.objects.get(pk=data["pk"])
        serializer = self.get_serializer(data={
            'content_model': ContentType.objects.get_for_model(model).pk,
            'content_id': data["pk"],
            'reporting_user': user.pk,
            'reported_user': instance.get_owner().pk,
            'reason': Reason.objects.get(pk=data["reason"]).pk,
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)



