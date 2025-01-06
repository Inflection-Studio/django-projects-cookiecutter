from django.db import models
from django.utils.timezone import now

from . import constants as common_db_constants


class PublishableQuerySet(models.QuerySet):
    """
    Custom QuerySet for Publishable models, providing methods
    to filter objects based on their publication status.
    """

    def published(self):
        """
        Retrieve all objects with the `PUBLISHED` status and
        a publication date in the past.

        Returns:
                QuerySet: A queryset of published objects.
        """
        return self.filter(
            publication_status=common_db_constants.PublicationStatusChoices.PUBLISHED,
        )

    def draft(self):
        """
        Retrieve all objects with the `DRAFT` status.

        Returns:
                QuerySet: A queryset of draft objects.
        """
        return self.filter(
            publication_status=common_db_constants.PublicationStatusChoices.DRAFT
        )

    def unpublished(self):
        """
        Retrieve all objects with the `UNPUBLISHED` status.

        Returns:
                QuerySet: A queryset of unpublished objects.
        """
        return self.filter(
            publication_status=common_db_constants.PublicationStatusChoices.UNPUBLISHED
        )

    def archived(self):
        """
        Retrieve all objects with the `ARCHIVED` status and
        an archive date in the past.

        Returns:
                QuerySet: A queryset of archived objects.
        """
        return self.filter(
            publication_status=common_db_constants.PublicationStatusChoices.ARCHIVED,
        )

    def recently_published(self, days: int = 7):
        """
        Retrieve objects published within the last N days.

        Args:
                days (int): The number of days to look back.

        Returns:
                QuerySet: A queryset of recently published objects.
        """
        from datetime import timedelta

        recent_date = now() - timedelta(days=days)
        return self.filter(
            publication_status=common_db_constants.PublicationStatusChoices.PUBLISHED,
            published_at__gte=recent_date,
        )

    def published_in_year(self, year: int):
        """
        Retrieve objects published in a specific year.

        Args:
                year (int): The year to filter by.

        Returns:
                QuerySet: A queryset of objects published in the specified year.
        """
        return self.filter(
            publication_status=common_db_constants.PublicationStatusChoices.PUBLISHED,
            published_at__year=year,
        )


class PublishableManager(models.Manager.from_queryset(PublishableQuerySet)):
    """
    Custom Manager for Publishable models, extending the
    PublishableQuerySet for additional convenience methods.
    """

    ...