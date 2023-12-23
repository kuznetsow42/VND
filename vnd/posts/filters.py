from datetime import timedelta

from django.utils import timezone
from django_filters import rest_framework as filters

from .models import Post


class PostFilter(filters.FilterSet):
    days = filters.NumberFilter(
        field_name='created_at', method='get_date', label="Creation interval")

    def get_date(self, queryset, field_name, value):
        time_threshold = timezone.now() - timedelta(days=int(value))
        return queryset.filter(created_at__gte=time_threshold)

    class Meta:
        model = Post
        fields = [
            "tags", "categories", "authors"
        ]

