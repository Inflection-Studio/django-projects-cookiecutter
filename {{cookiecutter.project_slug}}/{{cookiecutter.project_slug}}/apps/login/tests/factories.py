import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Sequence(lambda number: f"user{number}@example.com")
    {%- if cookiecutter.username_type == "username" %}
    username = factory.Sequence(lambda number: f"user{number}")
    {%- endif %}
    password = "test-password"
