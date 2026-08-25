# Django Projects Cookiecutter

This repository is a Cookiecutter template for generating opinionated Django
projects. It is not itself a Django application. The generated project lives
under `{{cookiecutter.project_slug}}/` and is rendered using the choices in
`cookiecutter.json`.

## Requirements

- Python 3.13
- Poetry 2.x

## Maintainer setup

```bash
poetry install
```

Generate a project with the default options:

```bash
poetry run cookiecutter . --no-input
```

Run the template test suite and lint the maintainer code:

```bash
poetry run pytest
poetry run ruff check hooks tests
poetry run ruff format --check hooks tests
```

## Repository layout

- `cookiecutter.json`: template variables and supported choices.
- `hooks/pre_gen_project.py`: validates inputs before rendering.
- `hooks/post_gen_project.py`: removes files that do not match the selected
  options and prepares generated-project artifacts.
- `tests/`: bakes representative option combinations and validates the output.
- `{{cookiecutter.project_slug}}/`: the generated Django project template.

## Changing a template option

When adding or changing a choice:

1. Update `cookiecutter.json`.
2. Add pre-generation validation for incompatible values when needed.
3. Update post-generation cleanup for conditional files.
4. Add or update a representative case in `tests/test_generation.py`.
5. Verify that rendered paths and text contain no `cookiecutter.` markers.
6. Run the generated project's checks and tests for affected combinations.

The generated project has its own README and `AGENTS.md`. Keep maintainer
instructions here and end-user instructions in the generated project.
