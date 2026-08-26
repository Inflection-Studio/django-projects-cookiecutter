# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

This project uses Django 6.1, Python 3.14, and uv for dependency
management.

## Requirements

- Python 3.14
- uv 0.12.6 or newer
- Git
{% if cookiecutter.use_docker == "y" %}- Docker with Docker Compose
{% endif %}

## Local setup

1. Create the local environment file:

   ```bash
   cp .env.example .env
   ```

2. Generate a Django secret key and add it to `SECRET_KEY` in `.env`:

   ```bash
   python -c "from secrets import token_urlsafe; print(token_urlsafe(50))"
   ```

3. Install the dependencies, apply migrations, and create an administrator:

   ```bash
   make deps
   make migrate
   make superuser
   ```

4. Start the development server:

   ```bash
   make runserver
   ```

The application is available at <http://127.0.0.1:8000/> and Django admin at
<http://127.0.0.1:8000/admin/>.

## Common commands

```bash
make test             # Run the test suite
make migrations       # Create migrations after model changes
make migrate          # Apply migrations
make shell            # Open Django shell_plus
make show_urls         # List registered URLs
make fmt-all           # Run all pre-commit checks and fixes
make hooks             # Install the Git pre-commit hook
```

Run a focused test directly with uv:

```bash
uv run --locked pytest {{ cookiecutter.project_slug }}/apps/login/tests/test_models.py
```

## Email delivery

Production email uses {% if cookiecutter.mail_service == "Other SMTP" %}Django's SMTP backend{% else %}django-anymail with the {{ cookiecutter.mail_service }} API backend{% endif %}.
Local development and tests use Django's in-memory backend so they never send
external email. Configure the provider-specific variables shown in
`.env.example` before deploying.
{% if cookiecutter.use_docker == "y" %}

## Docker workflows

The base Compose file defines Django, PostgreSQL, and nginx. Development and
staging behavior is layered on through override files.

```bash
make docker-dev            # Development stack with Compose watch
make docker-deploy         # Image-based deployment stack
make docker-staging        # Staging stack with source mounts
make docker-staging-build  # Rebuild and start the staging stack
make docker-down           # Stop the development stack
```

Always place the base file first when invoking Compose directly:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml config
```
{% endif %}

## Project layout

- `{{ cookiecutter.project_slug }}/apps/`: project-owned Django apps.
- `{{ cookiecutter.project_slug }}/common/`: reusable Django and database
  helpers.
- `{{ cookiecutter.project_slug }}/conf/settings/`: local, test, staging, and
  live settings.
- `templates/`: shared server-rendered templates.
- `mixins/`: reusable view mixins.
- `AGENTS.md`: repository guidance for coding agents and contributors.

{% if cookiecutter.username_type == "email" %}Authentication uses email as the
login identifier. Avoid adding username assumptions to forms, views, or APIs.
{% else %}Authentication uses Django's username field; email is collected as an
additional user attribute.
{% endif %}

## Configuration and deployment

Copy `.env.example` for each environment and replace every placeholder before
starting the application. Never commit `.env` files or credentials.

For deployment, set `ENVIRONMENT=prd`, use the live settings module, set
`DEBUG=False`, configure trusted hosts, and provide PostgreSQL and mail
credentials. Run Django's deployment checks before release:

```bash
uv run --locked python manage.py check --deploy
```

See `AGENTS.md` for architecture, testing, migration, and safety conventions.
