from typing import Any

from django.db.models import Count


def get_model_publication_analytics(model) -> dict[str, Any]:
	"""
	Generate analytics for a single model based on its publication statuses.

	Args:
		model: A Django model class with a `publication_status` field.

	Returns:
		dict: A dictionary with counts for each publication status.

	Raises:
		ValueError: If the model does not have a `publication_status` field.
	"""
	if not hasattr(model, "publication_status"):
		raise ValueError(
			f"Model {model.__name__} does not have a 'publication_status' field."
		)

	# Query to fetch counts for each publication status
	status_counts = model.objects.values("publication_status").annotate(
		count=Count("id")
	)

	# Map the counts to a dictionary
	analytics = {
		status["publication_status"]: status["count"]
		for status in status_counts
	}

	return analytics
