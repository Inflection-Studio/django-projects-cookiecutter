# How to Contribute

Issues and pull requests are welcome. This repository is a Cookiecutter template,
so changes must be verified both in the template itself and in the Django project
it generates.

## General considerations

1. Keep changes focused. Smaller pull requests are easier to review and verify.
2. Explain the problem being solved and, when applicable, link the related issue.
3. Preserve backwards compatibility unless the pull request clearly documents an
   intentional breaking change.
4. Never commit credentials, `.env` files, generated projects, virtual
   environments, caches, or local databases.
5. If you are new to pull requests, see GitHub's
   [guide to creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

## Getting started

1. Fork the repository.
2. Clone your fork.
3. Create a branch from an up-to-date `main` branch.

Do not develop directly on `main`. A focused branch such as `feat/add-option`,
`fix/generated-settings`, or `docs/update-setup` keeps the work isolated and
makes future contributions easier.

## Development setup

The maintainer tooling requires Python 3.14 and uv 0.12.6 or newer. Install uv
using the
[official installation instructions](https://docs.astral.sh/uv/getting-started/installation/),
then install the locked dependencies:

```bash
uv sync --locked
uv run --locked pre-commit install
```

uv creates the maintainer virtual environment at `.venv/`. You do not need to
activate it when using `uv run`. The installed Git hook runs the repository's
validation checks before each commit.

## Working on the template

The repository root is not a Django application. Files under
`{{cookiecutter.project_slug}}/` are rendered using the choices in
`cookiecutter.json`.

When adding or changing a template option:

1. Update `cookiecutter.json`.
2. Add pre-generation validation for invalid combinations when needed.
3. Update `hooks/post_gen_project.py` when conditional files must be removed.
4. Add representative coverage to `tests/test_generation.py`.
5. Update both maintainer and generated-project documentation as appropriate.
6. Verify the affected generated-project combinations.

Preserve Jinja expressions in template files. Always inspect the rendered output
rather than assuming a template source file is valid Python, YAML, or TOML before
rendering.

Model changes must include migrations. Generate migrations from a rendered
project, adapt them back into the template where Jinja values are required, and
verify the result with `makemigrations --check --dry-run`.

## Testing the template

Run the complete generation suite:

```bash
uv run --locked pytest
```

Run a focused test by name:

```bash
uv run --locked pytest tests/test_generation.py -k test_supported_combinations_render
```

Lint and check the formatting of maintainer code:

```bash
uv run --locked ruff check hooks tests
uv run --locked ruff format --check hooks tests
uv run --locked pre-commit run --all-files
```

The generation suite uses `pytest-cookies` to render representative option
combinations. It checks for unresolved Cookiecutter markers, parses rendered
Python, YAML, and TOML, and runs Ruff against generated projects.

## Testing a generated project

Dependency, Django, migration, or template-option changes should also be checked
inside a freshly rendered project. For example:

```bash
mkdir -p /tmp/django-cookiecutter-output
uv run --locked cookiecutter . \
  --no-input \
  --output-dir /tmp/django-cookiecutter-output \
  project_name="Contribution Smoke" \
  project_slug=contribution_smoke

cd /tmp/django-cookiecutter-output/contribution_smoke
uv sync --locked
uv run --locked python manage.py check
uv run --locked python manage.py makemigrations --check --dry-run
uv run --locked pytest
```

Select any additional Cookiecutter options needed to exercise the affected
behavior. Test both enabled and disabled states for conditional features where
applicable.

### Docker changes

Docker or deployment changes require a project generated with `use_docker=y`.
After installing its dependencies, validate both Compose overlays and build the
image:

```bash
cp .env.example .env
docker compose -f docker-compose.yml -f docker-compose.dev.yml config --quiet
docker compose -f docker-compose.yml -f docker-compose.staging.yml config --quiet
docker build --tag cookiecutter-django-smoke:local .
docker run --rm \
  --entrypoint python \
  --env DJANGO_SETTINGS_MODULE=contribution_smoke.conf.settings.test \
  cookiecutter-django-smoke:local \
  manage.py check
```

## Submitting a pull request

Before opening a pull request:

- Rebase or update your branch from `main` and resolve conflicts.
- Run the relevant template and generated-project checks.
- Include tests for new behavior and regressions.
- Update documentation when commands, options, dependencies, or generated
  behavior change.
- Commit `uv.lock` when maintainer dependencies change. Generated projects create
  their own `uv.lock` during rendering.
- Review the diff for generated files, secrets, debug output, and unrelated
  changes.

In the pull request description, explain what changed, why it changed, which
Cookiecutter combinations were tested, and the commands used for verification.
GitHub Actions will run the template suite and generated Django and Docker smoke
tests. If CI fails, update the branch with a fix or explain why the failure is
unrelated.

## Automated contributions

Automated coding agents should follow the repository's `AGENTS.md` instructions
and disclose material agent-generated changes in the pull request. Automated
contributions are held to the same review, testing, and security requirements as
other contributions.
