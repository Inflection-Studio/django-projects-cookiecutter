from django.db.models import Count, Q
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from {{ cookiecutter.project_slug }}.apps.blog import models
from {{ cookiecutter.project_slug }}.apps.blog.api.v1 import filters, serializers
from {{ cookiecutter.project_slug }}.common.db.constants import PublicationStatusChoices


class ArticleViewSet(ModelViewSet):
    serializer_class = serializers.ArticleSerializer
    queryset = models.Blog.objects.filter(
        publication_status=PublicationStatusChoices.PUBLISHED,
    ).order_by("-published_at")
    lookup_field = "slug"
    http_method_names = ["get"]
    filterset_class = filters.ArticleFilter



class ArticleCategoryListAPIView(generics.ListAPIView):
    serializer_class = serializers.ArticleCategorySerializer

    def get_queryset(self):
        return models.ArticleCategory.objects.annotate(
            published_articles_count=Count(
                "articles",
                filter=Q(articles__publication_status=PublicationStatusChoices.PUBLISHED),
            )
        ).filter(published_articles_count__gt=0)
