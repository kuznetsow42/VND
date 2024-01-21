from rest_framework import serializers

from reports.models import Reason, Report


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
