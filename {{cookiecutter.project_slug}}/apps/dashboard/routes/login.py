from django.urls import path

from ..views import (
    StaffCreateTemplateView,
    StaffDetailTemplateView,
    StaffListTemplateView,
    StaffUpdateTemplateView,
)

app_name = "login"

urlpatterns = [
    path("staff/", StaffListTemplateView.as_view(), name="staff_list"),
    path("staff/new/", StaffCreateTemplateView.as_view(), name="staff_create"),
    path("staff/<uuid:pk>/", StaffDetailTemplateView.as_view(), name="staff_details"),
    path(
        "staff/edit/<uuid:pk>/",
        StaffUpdateTemplateView.as_view(),
        name="staff_update",
    ),
]
