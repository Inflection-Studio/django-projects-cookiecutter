from enum import StrEnum

from django.db import models
from django.utils.translation import gettext_lazy as _


class PublicationStatusChoices(models.TextChoices):
	DRAFT = "Draft", _("Draft")
	PUBLISHED = "Published", _("Published")
	UNPUBLISHED = "Unpublished", _("Unpublished")
	ARCHIVED = "Archived", _("Archived")


class PublicationActions(StrEnum):
	PUBLISH = "publish"
	ARCHIVE = "archive"
	UNPUBLISH = "unarchive"
	DRAFT = "draft"

	@classmethod
	def choices(cls):
		return [item.value for item in cls]