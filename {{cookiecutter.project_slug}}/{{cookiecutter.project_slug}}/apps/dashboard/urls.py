from django.urls import include, path

app_name = "dashboard"

urlpatterns = [
    path("", include("{{ cookiecutter.project_slug }}.apps.dashboard.routes.index")),
    # user urls
    path("users/", include("{{ cookiecutter.project_slug }}.apps.dashboard.routes.login"))

]
