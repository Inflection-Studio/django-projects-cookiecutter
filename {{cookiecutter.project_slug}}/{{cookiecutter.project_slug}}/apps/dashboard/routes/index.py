from django.urls import path

from {{ cookiecutter.project_slug }}.apps.dashboard.views import IndexTemplateView

urlpatterns = [
    path("", IndexTemplateView.as_view(), name="home_page"),
]
