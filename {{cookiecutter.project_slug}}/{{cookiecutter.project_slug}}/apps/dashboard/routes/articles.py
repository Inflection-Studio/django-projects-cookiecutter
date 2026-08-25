from django.urls import path

from {{ cookiecutter.project_slug }}.apps.dashboard.views.blog import (
    articles as article_views,
)

app_name = "articles"

urlpatterns = [
    path(
        "list",
        article_views.ArticleListView.as_view(),
        name="article_list",
    ),
    path(
        "add",
        article_views.ArticleCreateView.as_view(),
        name="article_add",
    ),
    path(
        "<slug>/edit",
        article_views.ArticleUpdateView.as_view(),
        name="article_edit",
    ),
    path(
        "<slug>/details",
        article_views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path(
        "<slug>/delete",
        article_views.ArticleDeleteTemplateView.as_view(),
        name="article_delete",
    ),
    path(
        "articles/<int:pk>/<str:action>/",
        article_views.handle_article_action,
        name="handle_article_action",
    ),
    path(
        "categories/list",
        article_views.ArticleCategoryListView.as_view(),
        name="category_list",
    ),
    path(
        "categories/add",
        article_views.ArticleCategoryCreateView.as_view(),
        name="category_add",
    ),
    path(
        "categories/<slug>/edit",
        article_views.ArticleCategoryUpdateView.as_view(),
        name="category_edit",
    ),
    path(
        "categories/<slug>/details",
        article_views.ArticleCategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "categories/<slug>/add-article",
        article_views.ArticleCategoryArticleCreateView.as_view(),
        name="category_article_add",
    ),
]
