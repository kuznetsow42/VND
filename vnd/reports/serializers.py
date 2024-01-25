from rest_framework import serializers

from reports.models import Reason, Report, ClosedReport
from reports.utils import get_serialized_data


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = "__all__"


class CreateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    content_instance = serializers.SerializerMethodField()
    content_model = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ["content_model", "content_instance", "reported_at", "reason"]

    def get_content_instance(self, obj):
        return get_serialized_data(obj.content_model, obj.content_instance, self.context)

    def get_content_model(self, obj):
        return obj.content_model.name


class ClosedReportsSerializer(serializers.ModelSerializer):
    report = ReportSerializer()

    class Meta:
        model = ClosedReport
        fields = ["timestamp", "report", "approved", "objected"]
