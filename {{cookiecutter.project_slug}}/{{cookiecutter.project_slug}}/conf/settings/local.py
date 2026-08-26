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

# Keep local email deterministic and prevent accidental external delivery.
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    },
}
