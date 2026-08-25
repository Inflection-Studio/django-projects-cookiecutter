# Agent guidance

## What this repository is

This is a Cookiecutter template, not a runnable Django application. Source files
inside `{{cookiecutter.project_slug}}/` contain Jinja expressions that are
rendered using `cookiecutter.json`.

## Commands

```bash
poetry install
poetry run pytest
poetry run ruff check hooks tests
poetry run ruff format --check hooks tests
poetry run cookiecutter . --no-input --output-dir=/tmp/cookiecutter-output
```

Run generated-project Django commands from the rendered output, not from this
repository root.

## Template workflow

1. `hooks/pre_gen_project.py` validates the context.
2. Cookiecutter renders paths and file contents under the template directory.
3. `hooks/post_gen_project.py` removes artifacts that do not apply to the
   selected options and creates required generated artifacts.
4. `tests/test_generation.py` validates representative combinations.

Whenever a template option changes, update its validation, cleanup, generated
content, and test coverage together. Include at least the default configuration,
the affected option enabled, and incompatible or boundary combinations.

## Editing rules

- Preserve Jinja syntax in template sources and verify the rendered result.
- Do not assume a template source file is valid Python before rendering.
- Do not place product-specific Revlyn behavior in every generated project.
- Prefer generic app, service, integration, testing, and deployment patterns.
- Keep Django templates that need literal `{{ ... }}` or `{% ... %}` protected
  by the template's copy-without-render rules.
- Never commit generated projects, `.env` files, credentials, caches, or local
  databases.
- Add migrations for generated model changes; do not edit migration history
  without verifying a clean generated project with `makemigrations --check`.

## Verification

Before finishing a change:

- Bake every affected configuration.
- Check rendered filenames and text for leftover `cookiecutter.` references.
- Parse rendered Python files.
- Run Ruff on maintainer code.
- For dependency or Django changes, install one representative generated
  project and run `manage.py check`, `makemigrations --check`, and pytest.
- For Docker changes, render with `use_docker=y` and validate the Compose files.
