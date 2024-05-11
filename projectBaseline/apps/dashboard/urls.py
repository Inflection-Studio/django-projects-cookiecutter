from django.urls import path

from .views import IndexTemplateView

app_name = "dashboard"

urlpatterns = [
    path("", IndexTemplateView.as_view(), name="home_page"),
]
