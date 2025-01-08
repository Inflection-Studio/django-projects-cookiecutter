from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager
from tinymce.models import HTMLField

from ...common.db.models import (
    Publishable,
    UniqueSlugModel,
    unique_slug_generator,
)
from ...common.db.utils import upload_to_directory

User = get_user_model()


class BaseContent(UniqueSlugModel, Publishable, TimeStampedModel):
    title = models.CharField(max_length=255)
    body = HTMLField(verbose_name="content")
    cover_image = models.ImageField(
        upload_to=upload_to_directory, blank=True, null=True
    )
    tags = TaggableManager(blank=True)
    uploaded_by = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_uploaded",
        on_delete=models.PROTECT,
    )

    class Meta:
        abstract = True


class ArticleCategory(UniqueSlugModel, TimeStampedModel):
    name = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(
        User,
        related_name="article_categories_uploaded",
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = _("Article Category")
        verbose_name_plural = _("Article Categories")
        ordering = ["name", "-created"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy(
            "dashboard:articles:category_detail", kwargs={"slug": self.slug}
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(
                *args, instance=self, field_names=[self.name], **kwargs
            )
        super().save(*args, **kwargs)


class Blog(BaseContent):
    category = models.ForeignKey(
        ArticleCategory, related_name="articles", on_delete=models.PROTECT, null=True
    )

    def get_absolute_url(self):
        return reverse_lazy(
            "dashboard:articles:article_detail", kwargs={"slug": self.slug}
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")


class NewsletterSubscription(TimeStampedModel):
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    subscribed_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Subscribed At")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    def __str__(self):
        return self.email
