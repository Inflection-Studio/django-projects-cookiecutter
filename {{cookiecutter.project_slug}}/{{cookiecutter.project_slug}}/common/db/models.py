from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from . import constants as common_db_constants
from .managers import PublishableManager


def unique_slug_generator(instance, new_slug: str = None, field_names: list = None):
    """
    Generate a unique slug for a model instance.

    :param instance: The model instance for which to generate the slug.
    :param new_slug: An optional predefined slug.
    :param field_names: A list of field names to be concatenated for slug generation.
    :return: A unique slug string.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        if field_names is None or not field_names:
            field_names = [
                "title",
            ]  # Default to the "title" field if none are specified

        # Resolve field names to their values; if a value literal is passed,
        # preserve backward compatibility by using it directly.
        field_values = []
        for field in field_names:
            value = getattr(instance, field, field)
            if value and isinstance(value, str):
                value = value.strip()
                if value:
                    field_values.append(value)

        # Join non-empty field values to create the base slug
        combined_fields = " ".join(field_values)

        if not combined_fields:
            raise ValueError("The specified fields do not contain valid values.")

        # Add a random string for uniqueness
        random_string = get_random_string(length=6)
        slug = slugify(f"{combined_fields} {random_string}")

    # Trim slug to fit the maximum length of the slug field
    Klass = instance.__class__
    max_length = Klass._meta.get_field("slug").max_length
    slug = slug[:max_length]

    # Ensure uniqueness
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug[: max_length - 7]}-{get_random_string(length=6)}"
        return unique_slug_generator(
            instance, new_slug=new_slug, field_names=field_names,
        )

    return slug


class UniqueSlugModel(models.Model):
    slug = models.SlugField(
        verbose_name=_("Slug"),
        max_length=255,
        unique=True,
        blank=True,
        editable=False,
        db_index=True,
    )

    class Meta:
        abstract = True

    def save(self, generate_unique_slug=True, *args, **kwargs):
        field_names: list = kwargs.pop("field_names", [])
        if not field_names:
            field_names = ["title"]
        if generate_unique_slug and not self.slug:
            self.slug = unique_slug_generator(instance=self, field_names=field_names)
        super().save(*args, **kwargs)


class Publishable(models.Model):
    publication_status = models.CharField(
        verbose_name=_("Publication Status"),
        max_length=15,
        choices=common_db_constants.PublicationStatusChoices.choices,
        default=common_db_constants.PublicationStatusChoices.DRAFT,
    )
    published_at = models.DateTimeField(
        verbose_name=_("Published At"), null=True, blank=True,
    )
    archived_at = models.DateTimeField(
        verbose_name=_("Archived At"), null=True, blank=True,
    )

    objects = PublishableManager()

    class Meta:
        abstract = True
        ordering = ("-published_at",)
