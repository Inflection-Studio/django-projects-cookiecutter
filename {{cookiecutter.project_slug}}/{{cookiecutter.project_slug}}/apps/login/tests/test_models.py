import pytest
from django.contrib.auth import get_user_model

from {{ cookiecutter.project_slug }}.apps.login.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_user_factory_creates_valid_user():
    user = UserFactory()

    assert user.pk is not None
    assert user.check_password("test-password")
    assert str(user)


def test_create_superuser_sets_required_flags():
    user_model = get_user_model()
    {%- if cookiecutter.username_type == "email" %}
    user = user_model.objects.create_superuser(
        email="admin@example.com",
        password="test-password",
        first_name="Admin",
        last_name="User",
    )
    {%- else %}
    user = user_model.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="test-password",
        first_name="Admin",
        last_name="User",
    )
    {%- endif %}

    assert user.is_staff
    assert user.is_superuser
