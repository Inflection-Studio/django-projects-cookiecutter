from django.contrib import admin

from .models import ArticleCategory, Blog, NewsletterSubscription
from {{ cookiecutter.project_slug }}.utils.admin import UploadedByAdminMixin

@admin.register(Blog)
class BlogAdmin(UploadedByAdminMixin):
    """Admin configuration for the Blog model."""

    list_display = ("title", "uploaded_by", "publication_status", "created")
    list_filter = ("publication_status", "tags", "created")
    search_fields = ("title", "body", "tags__name")
    readonly_fields = ("slug", "created", "modified", "uploaded_by")
    autocomplete_fields = ("uploaded_by",)
    fieldsets = (
        (
            None,
            {"fields": ("title", "slug", "body", "cover_image", "tags", "uploaded_by")},
        ),
        ("Publication", {"fields": ("publication_status", "published_at")}),
        ("Timestamps", {"fields": ("created", "modified")}),
    )


@admin.register(ArticleCategory)
class ArticlecategoryAdmin(admin.ModelAdmin):
    """Admin configuration for the article category models."""

    list_display = ("slug", "name", "uploaded_by")
    readonly_fields = ("slug", "created", "modified", "uploaded_by")
    autocomplete_fields = ("uploaded_by",)


@admin.register(NewsletterSubscription)
class NewsletterubscriptionAdmin(admin.ModelAdmin):
    """Admin configuration for the newsletter subscription models."""
    list_display = ("email", "subscribed_at", "is_active")
    list_filter = ('is_active',)
