"""
WSGI config for {{ cookiecutter.project_slug }} project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

environment = os.environ.get("ENVIRONMENT", "local").lower()

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"{{ cookiecutter.project_slug }}.conf.settings.{environment}",
)

application = get_wsgi_application()
