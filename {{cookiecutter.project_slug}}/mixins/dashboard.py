# controls who views the dashboard
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.models import Site
from django.views.generic.base import ContextMixin, View


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