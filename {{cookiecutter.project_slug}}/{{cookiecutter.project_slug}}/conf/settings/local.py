# flake8: noqa
"""
Local Django settings.
Remember to update `{{ cookiecutter.project_slug }}.conf.settings.live` if necessary with defaults removed.
"""
from .common import *

# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}

# Keep local mail in memory unless SMTP was explicitly enabled in common settings.
if not USE_SMTP:
    MAILERS = {
        "default": {
            "BACKEND": "django.core.mail.backends.locmem.EmailBackend",
        },
    }
