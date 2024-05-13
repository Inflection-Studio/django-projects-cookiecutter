from django.urls import include, path

app_name = "dashboard"

urlpatterns = [
    path("", include("projectBaseline.apps.dashboard.routes.index")),
    # user urls
    path("users/", include("projectBaseline.apps.dashboard.routes.login"))

]
