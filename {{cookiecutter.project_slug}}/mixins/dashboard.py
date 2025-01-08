# controls who views the dashboard
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.models import Site
from django.views.generic.base import ContextMixin, View
from {{ cookiecutter.project_slug}}.common.db.constants import PublicationStatusChoices 
from {{ cookiecutter.project_slug}}.common.db.utils import get_status_action_map,  get_delete_view_action

class SuccessMessageMixin:
    """
    Add a success message on successful form submission.
    """

    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class AdminDashBoardMixin(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, ContextMixin, View
):

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["site"] = Site.objects.get_current()
        context["badge_classes"] = {
			PublicationStatusChoices.PUBLISHED: "badge-success",
			PublicationStatusChoices.DRAFT: "badge-info",
			PublicationStatusChoices.UNPUBLISHED: "badge-warning",
			PublicationStatusChoices.ARCHIVED: "badge-danger",
		}
        return context

    def test_func(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return True
        return False

class FormViewDashboardMixin(ContextMixin):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

class PublishableContentMixin:
	"""
	Mixin for handling publishable content actions in detail views.
	Provides status-based actions and a delete action.
	"""

	def get_publishable_actions(self):
		"""
		Returns a list of actions based on the object's publication status.
		Includes a delete action by default.
		"""
		# Ensure the object exists
		obj = self.get_object()

		# Get the status-action mapping
		status_action_map: dict = get_status_action_map()

		# Retrieve actions for the current publication status
		actions = status_action_map.get(obj.publication_status, [])

		# Append delete action
		actions.append(get_delete_view_action())

		return actions

	def get_publishable_status_info(self):
		"""
		Returns a dictionary of status information for the object.
		"""
		obj = self.get_object()
		status_field_map = {
			PublicationStatusChoices.PUBLISHED: {
				"label": "Published On",
				"field": obj.published_at,
			},
			PublicationStatusChoices.ARCHIVED: {
				"label": "Archived On",
				"field": obj.archived_at,
			},
		}
		status_info = status_field_map.get(obj.publication_status, {})
		return status_info

	def get_context_data(self, **kwargs):
		"""
		Add publishable actions to the context data.
		"""
		context = super().get_context_data(**kwargs)
		context["actions"] = self.get_publishable_actions()
		context["status_info"] = self.get_publishable_status_info()
		return context