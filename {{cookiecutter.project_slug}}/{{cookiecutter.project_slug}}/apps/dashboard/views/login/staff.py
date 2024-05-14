from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from mixins.dashboard import AdminDashBoardMixin
from {{ cookiecutter.project_slug }}.apps.login.utils.email import EmailService

User = get_user_model()


class StaffCreateTemplateView(AdminDashBoardMixin, CreateView):
    model = User
    template_name = "dashboard/login/staff/form.html"
    success_message = "Staff Created Successfully"
    fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "is_superuser",
    ]

    def form_valid(self, form):
        email_service = EmailService(self.request)
        random_password = get_random_string(length=7)

        user = form.save(commit=False)
        user.username = user.email
        user.set_password(random_password)
        user.is_staff = True
        user.is_active = True
        user.save()
        email_service.send_user_registration_email(user=user, password=random_password)
        return super().form_valid(form)


class StaffListTemplateView(AdminDashBoardMixin, ListView):
    model = User
    template_name = "dashboard/login/staff/list.html"
    context_object_name = "staffs"


class StaffDetailTemplateView(AdminDashBoardMixin, DetailView):
    model = User
    template_name = "dashboard/login/staff/detail.html"
    context_object_name = "staff"


class StaffUpdateTemplateView(AdminDashBoardMixin, UpdateView):
    model = User
    template_name = "dashboard/login/staff/form.html"
    context_object_name = "staff"
    success_message = "Staff Updated Successfully"
    fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "is_superuser",
        "is_active",
    ]
