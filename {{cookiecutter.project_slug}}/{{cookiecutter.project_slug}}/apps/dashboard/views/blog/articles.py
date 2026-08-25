from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from {{ cookiecutter.project_slug }}.apps.blog import forms, models

from {{ cookiecutter.project_slug }}.apps.blog.analytics.utils import get_model_publication_analytics
from {{ cookiecutter.project_slug }}.common.db.utils import route_publication_action
from {{ cookiecutter.project_slug }}.common.db.constants import PublicationStatusChoices
from mixins.dashboard import AdminDashBoardMixin, PublishableContentMixin

User = get_user_model()


class ArticleCreateUpdateView(AdminDashBoardMixin, CreateView):
    model = models.Blog
    template_name = "dashboard/articles/form.html"
    success_message = "Article added successfully"
    form_class = forms.ArticleForm


class ArticleCreateView(ArticleCreateUpdateView, CreateView):
    def form_valid(self, form):
        article = form.save(commit=False)
        user = self.request.user
        article.uploaded_by = user

        article.save()
        return super().form_valid(form)


class ArticleUpdateView(ArticleCreateUpdateView, UpdateView):
    success_message = "Article updated successfully"
    context_object_name = "article"


class ArticleListView(AdminDashBoardMixin, ListView):
    model = models.Blog
    context_object_name = "articles"
    template_name = "dashboard/articles/list.html"

    @cached_property
    def article_analytics(self):
        return get_model_publication_analytics(model=models.Blog)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the lazy analytics object to the context
        publication_analytics = self.article_analytics
        context["draft_articles_count"] = publication_analytics.get(
            PublicationStatusChoices.DRAFT, 0
        )
        context["published_articles_count"] = publication_analytics.get(
            PublicationStatusChoices.PUBLISHED, 0
        )
        context["unpublished_articles_count"] = publication_analytics.get(
            PublicationStatusChoices.UNPUBLISHED, 0
        )
        context["archived_articles_count"] = publication_analytics.get(
            PublicationStatusChoices.ARCHIVED, 0
        )
        context["all_articles_count"] = (
            publication_analytics.get(PublicationStatusChoices.DRAFT, 0)
            + publication_analytics.get(PublicationStatusChoices.PUBLISHED, 0)
            + publication_analytics.get(PublicationStatusChoices.UNPUBLISHED, 0)
            + publication_analytics.get(PublicationStatusChoices.ARCHIVED, 0)
        )
        return context


class ArticleDetailView(AdminDashBoardMixin, PublishableContentMixin, DetailView):
    model = models.Blog
    context_object_name = "article"
    template_name = "dashboard/articles/detail.html"

    def get_queryset(self):
        # Use prefetch_related to optimize tag loading
        return models.Blog.objects.prefetch_related("tags")


class ArticleDeleteTemplateView(AdminDashBoardMixin, DeleteView):
    model = models.Blog
    template_name = "dashboard/confirm-delete.html"
    success_message = "Article successfully deleted"

    def get_success_url(self) -> str:
        return reverse_lazy("dashboard:articles:article_list")


def handle_article_action(request, action: str, pk: str | int):
    """
    Generic view to handle actions (publish, unpublish, archive, draft) for articles.

    Args:
            request: The HTTP request object.
            action: The action to perform, derived from the URL.
            pk: The primary key of the article.

    Returns:
            HTTP Response from the handle_publishable_handler function.

    Raises:
            Http404: If the action is not valid.
    """
    return route_publication_action(
        request=request, action=action, pk=pk, model_class=models.Blog
    )


class ArticleCategoryCreateUpdateView(AdminDashBoardMixin):
    model = models.ArticleCategory
    fields = ["name"]
    template_name = "dashboard/articles/categories/form.html"


class ArticleCategoryCreateView(ArticleCategoryCreateUpdateView, CreateView):
    success_message = "Article Category added successfully"

    def form_valid(self, form):
        category = form.save(commit=False)
        category.uploaded_by = self.request.user

        category.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_namespace"] = "article"
        context["title"] = "Add Article Category"
        return context


class ArticleCategoryUpdateView(ArticleCategoryCreateUpdateView, UpdateView):
    """Update the basic features of the ArticleCategory"""

    success_message = "Article Category details updated"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_namespace"] = "category"
        context["title"] = "Edit Article Category"
        return context


class ArticleCategoryListView(AdminDashBoardMixin, ListView):
    model = models.ArticleCategory
    context_object_name = "categories"
    template_name = "dashboard/articles/categories/list.html"


class ArticleCategoryDetailView(AdminDashBoardMixin, DetailView):
    model = models.ArticleCategory
    context_object_name = "category"
    template_name = "dashboard/articles/categories/detail.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("articles")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = self.object.articles.all()
        return context


class ArticleCategoryArticleCreateView(AdminDashBoardMixin, CreateView):
    model = models.Blog
    form_class = forms.ArticleForm
    template_name = "dashboard/articles/categories/form.html"
    success_message = "Article added successfully"

    def setup(self, request, *args, **kwargs):
        """Initialize ArticleCategory when the view is setup"""
        super().setup(request, *args, **kwargs)
        self.article_category = get_object_or_404(
            models.ArticleCategory, slug=kwargs["slug"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_category = self.article_category
        context.update(
            {
                "model_namespace": "category",
                "title": f"Add {article_category.name.title()} Article",
                "article_category": article_category,
            }
        )
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop("category", None)
        return form

    def form_valid(self, form):
        article = form.save(commit=False)
        article.category = self.article_category
        article.uploaded_by = self.request.user
        article.save()
        return super().form_valid(form)
