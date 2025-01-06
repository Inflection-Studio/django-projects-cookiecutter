from decimal import Decimal

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from . import constants as common_db_constants
from .fields import Publishable


class InvalidContentTypeError(TypeError):
	pass

def unique_slug_generator(instance, new_slug: str = None, field_name: str = "name"):
    if new_slug is not None:
        slug = new_slug
    else:
        random_string = get_random_string(length=6)
        slug = slugify(f"{getattr(instance, field_name)} {random_string}")
    Klass = instance.__class__
    max_length = Klass._meta.get_field("slug").max_length
    slug = slug[:max_length]
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = f"{slug[:max_length - 5]}-{get_random_string(length=6)}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def get_average_review_rating(reviews) -> Decimal:
    total_reviews = reviews.count()
    if total_reviews > 0:
        total_rating = sum([review.rating for review in reviews])
        return total_rating / Decimal(total_reviews)
    return Decimal(0.0)


def get_status_action_map() -> dict[str, list[dict]]:
	"""
	Get a map of publication status to available actions.
	Acts a simple state machine for publication status transitions.
	return: A dictionary mapping publication status to available actions.
	"""
	# Map actions based on the publication status using enums
	status_action_map = {
		common_db_constants.PublicationStatusChoices.ARCHIVED: [
			{
				"action": common_db_constants.PublicationActions.PUBLISH,
				"label": "Publish",
				"btn_class": "btn-success",
			},
			{
				"action": common_db_constants.PublicationActions.DRAFT,
				"label": "Unarchive (Convert to Draft)",
				"btn_class": "btn-warning",
			},
		],
		common_db_constants.PublicationStatusChoices.UNPUBLISHED: [
			{
				"action": common_db_constants.PublicationActions.PUBLISH,
				"label": "Publish",
				"btn_class": "btn-success",
			},
		],
		common_db_constants.PublicationStatusChoices.DRAFT: [
			{
				"action": common_db_constants.PublicationActions.PUBLISH,
				"label": "Publish",
				"btn_class": "btn-success",
			},
		],
		common_db_constants.PublicationStatusChoices.PUBLISHED: [
			{
				"action": common_db_constants.PublicationActions.UNPUBLISH,
				"label": "Unpublish",
				"btn_class": "btn-warning",
			},
			{
				"action": common_db_constants.PublicationActions.ARCHIVE,
				"label": "Archive",
				"btn_class": "btn-secondary",
			},
		],
	}
	return status_action_map


def unpublish_publishable_content(
	request,
	publishable_content: Publishable,
):
	publishable_content.publication_status = (
		common_db_constants.PublicationStatusChoices.UNPUBLISHED
	)
	publishable_content.modified = timezone.now()
	publishable_content.save(update_fields=["publication_status", "modified"])
	messages.success(request, f"{type(publishable_content).__name__} Unpublished")
	return redirect(publishable_content.get_absolute_url())


def publish_publishable_content(
	request: HttpRequest,
	publishable_content: Publishable,
):
	publishable_content.publication_status = (
		common_db_constants.PublicationStatusChoices.PUBLISHED
	)
	publishable_content.modified = timezone.now()
	publishable_content.published_at = timezone.now()
	publishable_content.save(
		update_fields=["publication_status", "modified", "published_at"]
	)
	messages.success(request, f"{type(publishable_content).__name__} Published")
	return redirect(publishable_content.get_absolute_url())


def archive_publishable_content(
	request: HttpRequest,
	publishable_content: Publishable,
):
	publishable_content.publication_status = (
		common_db_constants.PublicationStatusChoices.ARCHIVED
	)
	publishable_content.modified = timezone.now()
	publishable_content.archived_at = timezone.now()
	publishable_content.save(
		update_fields=["publication_status", "modified", "archived_at"]
	)
	messages.success(request, f"{type(publishable_content).__name__} Archived")
	return redirect(publishable_content.get_absolute_url())


def draft_publishable_content(
	request: HttpRequest,
	publishable_content: Publishable,
):
	publishable_content.publication_status = (
		common_db_constants.PublicationStatusChoices.DRAFT
	)
	publishable_content.modified = timezone.now()
	publishable_content.archived_at = timezone.now()
	publishable_content.save(update_fields=["publication_status", "modified"])
	messages.success(request, f"{type(publishable_content).__name__} Drafted")
	return redirect(publishable_content.get_absolute_url())


def handle_publishable_content_action(
	request: HttpRequest,
	action: str,
	model_class: "models.Model",
	pk: str | int,
) -> HttpResponse:
	"""
	Handles actions on Publishable content (publish/unpublish/archive).

	Args:
			request: The HTTP request object.
			action: The action to perform ('publish', 'unpublish', etc.).
			model_class: The Django model class.
			pk: The primary key of the model instance.

	Raises:
			InvalidContentTypeError: If the model is not a subclass of Publishable.
			ValueError: If the action is invalid.

	Returns:
			HTTP Response redirecting to the instance's URL.
	"""

	# Validate that the model is a subclass of Publishable
	if not issubclass(model_class, Publishable):
		raise InvalidContentTypeError(
			f"Expected a subclass of Publishable, but got {model_class.__name__!r}."
		)

	# Validate the action and get the corresponding function
	action_map = {
		common_db_constants.PublicationActions.PUBLISH: publish_publishable_content,
		common_db_constants.PublicationActions.UNPUBLISH: unpublish_publishable_content,
		common_db_constants.PublicationActions.ARCHIVE: archive_publishable_content,
		common_db_constants.PublicationActions.DRAFT: draft_publishable_content,
	}

	action_function = action_map.get(action)
	if not action_function:
		valid_actions = list(action_map.keys())
		raise ValueError(
			f"Invalid action '{action!r}'. Must be one of {valid_actions}."
		)

	# Retrieve the object instance
	publishable_content = get_object_or_404(model_class, pk=pk)

	# Perform the action
	return action_function(request, publishable_content)