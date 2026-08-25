# flake8: noqa
"""
Live Django settings.
Meant to be used inside a Docker container or in a live environment.
Similar to `{{ cookiecutter.project_slug }}.conf.settings.local` but with defaults removed.
"""
from .common import *

# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE", default="django.db.backends.postgresql_psycopg2"),
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.int("DB_PORT"),
    }
}
