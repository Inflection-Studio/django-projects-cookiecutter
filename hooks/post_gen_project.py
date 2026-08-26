import shutil
import subprocess
import sys
from pathlib import Path


def remove(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def create_uv_lock() -> None:
    uv = shutil.which("uv")
    if uv is None:
        print(
            "ERROR: uv is required to generate the project lock file.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    try:
        subprocess.run(
            [uv, "lock", "--no-progress"],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print("ERROR: uv could not generate uv.lock.", file=sys.stderr)
        raise SystemExit(exc.returncode) from exc


if "{{ cookiecutter.open_source_license }}" == "Not open source":
    remove(Path("LICENSE"))

if "{{ cookiecutter.username_type }}" == "username":
    remove(Path("{{ cookiecutter.project_slug }}", "apps", "login", "managers.py"))

if "{{ cookiecutter.has_blog }}" != "y":
    remove(Path("{{ cookiecutter.project_slug }}", "apps", "blog"))
    remove(
        Path(
            "{{ cookiecutter.project_slug }}",
            "apps",
            "dashboard",
            "routes",
            "articles.py",
        )
    )
    remove(
        Path(
            "{{ cookiecutter.project_slug }}",
            "apps",
            "dashboard",
            "views",
            "blog",
        )
    )
    remove(Path("templates", "dashboard", "articles"))
elif "{{ cookiecutter.use_drf }}" != "y":
    remove(Path("{{ cookiecutter.project_slug }}", "apps", "blog", "api"))

if "{{ cookiecutter.use_drf }}" != "y":
    remove(Path("{{ cookiecutter.project_slug }}", "common", "pagination.py"))
    remove(Path("{{ cookiecutter.project_slug }}", "common", "versioning.py"))

if "{{ cookiecutter.use_docker }}" != "y":
    for docker_path in (
        ".dockerignore",
        "Dockerfile",
        "deploy",
        "docker-compose.dev.yml",
        "docker-compose.staging.yml",
        "docker-compose.yml",
    ):
        remove(Path(docker_path))

create_uv_lock()
