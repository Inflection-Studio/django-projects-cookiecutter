from django.urls import include, path

app_name = "blog"

urlpatterns = [path("api/", include("{{ cookiecutter.project_slug }}.apps.blog.api.urls"))]
