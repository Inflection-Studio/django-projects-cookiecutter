# Agent guidance for {{ cookiecutter.project_name }}

## Project overview

This is a Django project using Python 3.14 and uv. Django applications live
under `{{ cookiecutter.project_slug }}/apps/`, shared framework code lives under
`{{ cookiecutter.project_slug }}/common/`, and environment-specific settings live
under `{{ cookiecutter.project_slug }}/conf/settings/`.

## Commands

```bash
make deps
make runserver
make migrations
make migrate
make test
make fmt-all
```

Run a focused test with:

```bash
uv run --locked pytest path/to/test_file.py -k test_name
```
{% if cookiecutter.use_docker == "y" %}
Docker workflows:

```bash
make docker-dev
make docker-staging
make docker-down
```

The Docker stack includes the web application, PostgreSQL, Redis, nginx, and
pgAdmin services. Redis is built from `deploy/redis/Dockerfile` and is available
for applications such as Celery to use as a broker/result backend.
{% endif %}

## Architecture

- Keep views and API handlers thin. Put multi-step business workflows in an
  app-level `services/` package.
- Put third-party provider clients and adapters in
  `{{ cookiecutter.project_slug }}/integrations/`, outside Django apps.
- Keep `urls.py` route-only; define handlers in `views.py` or `api/views.py`.
- Keep reusable database abstractions in `common/db/` and app-specific choices
  in each app's `constants.py`.
- Prefer mock provider adapters in tests. Tests must not call live external
  services.

## Django conventions

- Add a new migration for every model change and review it before committing.
- Never edit an already-applied migration unless the task explicitly requires a
  migration repair.
- Use `settings.AUTH_USER_MODEL` or `get_user_model()` instead of importing the
  concrete user model from another app.
- Keep secrets and deployment-specific values in environment variables.
- Do not weaken production security settings to make local development easier.
{% if cookiecutter.username_type == "email" %}
- Authentication uses email as `USERNAME_FIELD`; do not reintroduce username
  assumptions in forms, serializers, or queries.
{% else %}
- Authentication uses Django's username field. Email is also collected but is
  not the authentication identifier.
{% endif %}

## Tests and quality

- Place tests in the owning app's `tests/` package.
- Use `conftest.py` for local fixtures and `factories.py` for Factory Boy
  factories.
- Cover success, validation, permission, and failure paths for changed behavior.
- Run focused tests during development, then `make test` and `make fmt-all`.
- Use spaces for Python indentation, double quotes, and the configured Ruff
  formatter.

## Safety

- Never commit `.env`, credentials, API keys, local databases, generated media,
  or coverage output.
- Avoid logging passwords, tokens, secrets, or sensitive personal data.
- Treat migrations, authentication, permissions, billing, and deployment
  changes as high-risk and verify them with focused tests.
