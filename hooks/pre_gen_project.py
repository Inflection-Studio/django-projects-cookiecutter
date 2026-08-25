import sys


def abort(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


project_slug = "{{ cookiecutter.project_slug }}"
class_name_prefix = "{{ cookiecutter.class_name_prefix }}"

if not project_slug.isidentifier():
    abort(f"Project slug {project_slug!r} must be a valid Python identifier.")

if project_slug != project_slug.lower():
    abort(f"Project slug {project_slug!r} must be lowercase.")

if not class_name_prefix.isidentifier():
    abort(f"Class name prefix {class_name_prefix!r} must be a valid Python identifier.")

if not class_name_prefix[0].isupper():
    abort(f"Class name prefix {class_name_prefix!r} must start with a capital letter.")
