import django_filters

from {{ cookiecutter.project_slug }}.apps.blog import models


class ArticleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")

    class Meta:
        model = models.Blog
        fields = {"title": ["icontains"], "category": ["exact"]}
