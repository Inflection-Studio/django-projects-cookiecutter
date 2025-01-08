from django.urls import path
from rest_framework.routers import DefaultRouter

from {{ cookiecutter.project_slug }}.apps.blog.api.v1 import viewsets

app_name = "v1"

router = DefaultRouter()

router.register("articles", viewsets.ArticleViewSet, basename="articles")
urlpatterns =  [
    path('articles/categories/', viewsets.ArticleCategoryListAPIView.as_view(), name='category-list'),
] + router.urls
