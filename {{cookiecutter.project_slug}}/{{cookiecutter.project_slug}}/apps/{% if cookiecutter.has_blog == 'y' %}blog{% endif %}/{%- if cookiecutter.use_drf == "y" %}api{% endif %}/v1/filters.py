import django_filters
from django.utils import timezone

from kraps_api.apps.blog import models


class EventFilter(django_filters.FilterSet):
    upcoming = django_filters.BooleanFilter(
        method="filter_by_upcoming", label="upcoming"
    )
    past = django_filters.BooleanFilter(method="filter_by_past", label="past")
    date_range = django_filters.DateFromToRangeFilter(
        field_name="start_date", label="Date Range"
    )

    def filter_by_upcoming(self, queryset, name, value):
        if value:  # Only apply the filter if the value is True
            return queryset.filter(start_date__gte=timezone.now())
        return queryset

    def filter_by_past(self, queryset, name, value):
        if value:  # Only apply the filter if the value is True
            return queryset.filter(end_date__lt=timezone.now())
        return queryset

    def filter_by_date_range(self, queryset, name, value):
        if value.start and value.stop:
            queryset = queryset.filter(date__range=(value.start, value.stop))
        return queryset

    class Meta:
        model = models.Event
        fields = {
            "title": ["icontains"],
            "event_type": ["exact"],
            "location_type": ["exact"],
        }


class ArticleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")

    class Meta:
        model = models.Blog
        fields = {"title": ["icontains"], "category": ["exact"]}
