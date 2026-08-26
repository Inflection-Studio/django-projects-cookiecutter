import ast
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
import yaml

TEXT_EXCLUSIONS = {".eot", ".gif", ".jpg", ".map", ".min.js", ".png", ".ttf", ".woff"}


def assert_successful_bake(result) -> Path:
    assert result.exit_code == 0, result.exception
    assert result.exception is None
    assert result.project_path is not None
    assert result.project_path.is_dir()
    return result.project_path


def assert_no_cookiecutter_markers(project_path: Path) -> None:
    for path in project_path.rglob("*"):
        assert "cookiecutter." not in path.name
        is_excluded = any(str(path).endswith(suffix) for suffix in TEXT_EXCLUSIONS)
        if not path.is_file() or is_excluded:
            continue
        try:
            content = path.read_text()
        except UnicodeDecodeError:
            continue
        assert "cookiecutter." not in content, path


def assert_python_parses(project_path: Path) -> None:
    for path in project_path.rglob("*.py"):
        ast.parse(path.read_text(), filename=str(path))


def assert_yaml_parses(project_path: Path) -> None:
    for pattern in ("*.yaml", "*.yml"):
        for path in project_path.rglob(pattern):
            yaml.safe_load(path.read_text())


def assert_toml_parses(project_path: Path) -> None:
    for path in project_path.rglob("*.toml"):
        tomllib.loads(path.read_text())


def assert_ruff_clean(project_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "."],
        cwd=project_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def assert_optional_files(project_path: Path, context: dict[str, str]) -> None:
    package = project_path / project_path.name
    has_blog = context.get("has_blog", "n") == "y"
    use_docker = context.get("use_docker", "n") == "y"
    use_drf = context.get("use_drf", "n") == "y"

    assert (project_path / "Dockerfile").exists() is use_docker
    if use_docker:
        dockerfile = (project_path / "Dockerfile").read_text()
        assert "FROM python:3.14-slim AS base" in dockerfile
        assert (project_path / "deploy" / "redis" / "Dockerfile").is_file()
        compose = yaml.safe_load((project_path / "docker-compose.yml").read_text())
        redis = compose["services"]["redis"]
        assert redis["build"] == "./deploy/redis"
        assert redis["networks"] == ["internal"]
        assert redis["volumes"] == ["redisdata:/data"]
        assert redis["healthcheck"]["test"] == ["CMD", "redis-cli", "ping"]
        assert "redisdata" in compose["volumes"]
    assert (project_path / "uv.lock").is_file()
    assert not (project_path / "poetry.lock").exists()
    assert ".venv/" in (project_path / ".gitignore").read_text()
    assert (package / "apps" / "blog").exists() is has_blog
    assert (
        package / "apps" / "blog" / "migrations" / "0001_initial.py"
    ).exists() is has_blog
    assert (package / "common" / "pagination.py").exists() is use_drf
    assert (package / "common" / "versioning.py").exists() is use_drf
    assert (package / "apps" / "blog" / "api").exists() is (has_blog and use_drf)
    assert (package / "apps" / "login" / "migrations" / "0001_initial.py").is_file()


def assert_dependabot_config(project_path: Path, context: dict[str, str]) -> None:
    config_path = project_path / ".github" / "dependabot.yml"
    config = yaml.safe_load(config_path.read_text())
    updates = config["updates"]
    ecosystems = [update["package-ecosystem"] for update in updates]
    use_docker = context.get("use_docker", "n") == "y"

    assert ecosystems.count("github-actions") == 1
    assert ecosystems.count("uv") == 1
    assert ecosystems.count("docker") == (2 if use_docker else 0)
    assert ecosystems.count("docker-compose") == (1 if use_docker else 0)

    if use_docker:
        docker_updates = [
            update for update in updates if update["package-ecosystem"] == "docker"
        ]
        assert docker_updates[0]["directory"] == "/"
        assert set(docker_updates[1]["directories"]) == {
            "/deploy/nginx",
            "/deploy/postgres",
            "/deploy/redis",
        }

    codeql_workflow = (
        project_path / ".github" / "workflows" / "codeql.yml"
    ).read_text()
    assert "${{ matrix.language }}" in codeql_workflow


def assert_uv_project(project_path: Path) -> None:
    config = tomllib.loads((project_path / "pyproject.toml").read_text())

    assert config["tool"]["uv"]["package"] is False
    assert config["project"]["requires-python"] == ">=3.14,<4.0"
    assert "dev" in config["dependency-groups"]
    assert "test" in config["dependency-groups"]

    for relative_path in ("AGENTS.md", "Makefile", "README.md", "pyproject.toml"):
        assert "poetry" not in (project_path / relative_path).read_text().lower()


@pytest.mark.parametrize(
    "extra_context",
    [
        {},
        {"project_name": "Email Auth", "username_type": "email"},
        {"project_name": "Tags Only", "has_tags": "y"},
        {
            "project_name": "Full Stack",
            "username_type": "email",
            "has_blog": "y",
            "has_tags": "y",
            "use_docker": "y",
            "use_drf": "y",
            "use_martor_editor": "y",
            "use_phone_numbers_field": "y",
        },
    ],
)
def test_supported_combinations_render(cookies, extra_context):
    project_path = assert_successful_bake(cookies.bake(extra_context=extra_context))
    assert_no_cookiecutter_markers(project_path)
    assert_python_parses(project_path)
    assert_yaml_parses(project_path)
    assert_toml_parses(project_path)
    assert_optional_files(project_path, extra_context)
    assert_dependabot_config(project_path, extra_context)
    assert_uv_project(project_path)
    assert_ruff_clean(project_path)


@pytest.mark.parametrize(
    ("mail_service", "backend", "setting_name", "env_name"),
    [
        (
            "Mailgun",
            "anymail.backends.mailgun.EmailBackend",
            "MAILGUN_API_KEY",
            "MAILGUN_API_KEY",
        ),
        (
            "Amazon SES",
            "anymail.backends.amazon_ses.EmailBackend",
            "AMAZON_SES_CLIENT_PARAMS",
            "AWS_ACCESS_KEY_ID",
        ),
        (
            "Mailjet",
            "anymail.backends.mailjet.EmailBackend",
            "MAILJET_API_KEY",
            "MAILJET_API_KEY",
        ),
        (
            "Mandrill",
            "anymail.backends.mandrill.EmailBackend",
            "MANDRILL_API_KEY",
            "MANDRILL_API_KEY",
        ),
        (
            "Postmark",
            "anymail.backends.postmark.EmailBackend",
            "POSTMARK_SERVER_TOKEN",
            "POSTMARK_SERVER_TOKEN",
        ),
        (
            "SendGrid",
            "anymail.backends.sendgrid.EmailBackend",
            "SENDGRID_API_KEY",
            "SENDGRID_API_KEY",
        ),
        (
            "Brevo",
            "anymail.backends.brevo.EmailBackend",
            "BREVO_API_KEY",
            "BREVO_API_KEY",
        ),
        (
            "SparkPost",
            "anymail.backends.sparkpost.EmailBackend",
            "SPARKPOST_API_KEY",
            "SPARKPOST_API_KEY",
        ),
    ],
)
def test_anymail_provider_configuration(
    cookies, mail_service, backend, setting_name, env_name
):
    project_path = assert_successful_bake(
        cookies.bake(extra_context={"mail_service": mail_service})
    )
    package = project_path / project_path.name
    settings = (package / "conf" / "settings" / "common.py").read_text()
    environment = (project_path / ".env.example").read_text()
    pyproject = (project_path / "pyproject.toml").read_text()

    assert f'"BACKEND": "{backend}"' in settings
    assert "EMAIL_BACKEND =" not in settings
    assert f'"{setting_name}"' in settings
    assert f"{env_name}=" in environment
    assert '"anymail",' in settings
    assert "django-anymail" in pyproject
    if mail_service == "Amazon SES":
        assert "django-anymail[amazon-ses]" in pyproject
    assert_python_parses(project_path)
    assert_ruff_clean(project_path)


def test_other_smtp_uses_django_backend(cookies):
    project_path = assert_successful_bake(
        cookies.bake(extra_context={"mail_service": "Other SMTP"})
    )
    package = project_path / project_path.name
    settings = (package / "conf" / "settings" / "common.py").read_text()
    environment = (project_path / ".env.example").read_text()
    pyproject = (project_path / "pyproject.toml").read_text()

    assert '"BACKEND": "django.core.mail.backends.smtp.EmailBackend"' in settings
    assert "EMAIL_BACKEND =" not in settings
    assert "EMAIL_HOST=" in environment
    assert '"anymail",' not in settings
    assert "django-anymail" not in pyproject
    assert_python_parses(project_path)
    assert_ruff_clean(project_path)


def test_username_auth_uses_django_user_manager(cookies):
    project_path = assert_successful_bake(cookies.bake())
    package = project_path / "my_awesome_project"
    model = (package / "apps" / "login" / "models.py").read_text()
    settings = (package / "conf" / "settings" / "common.py").read_text()

    assert "CustomUserManager" not in model
    assert not (package / "apps" / "login" / "managers.py").exists()
    assert 'ACCOUNT_LOGIN_METHODS = {"username"}' in settings
    assert '"username*"' in settings


def test_email_auth_uses_custom_user_manager(cookies):
    result = cookies.bake(
        extra_context={"project_name": "Email Auth", "username_type": "email"}
    )
    project_path = assert_successful_bake(result)
    package = project_path / "email_auth"
    model = (package / "apps" / "login" / "models.py").read_text()
    settings = (package / "conf" / "settings" / "common.py").read_text()

    assert "username = None" in model
    assert "objects = CustomUserManager()" in model
    assert (package / "apps" / "login" / "managers.py").is_file()
    assert 'ACCOUNT_LOGIN_METHODS = {"email"}' in settings


def test_docker_project_has_uv_lock_file(cookies):
    result = cookies.bake(
        extra_context={"project_name": "Docker Project", "use_docker": "y"}
    )
    project_path = assert_successful_bake(result)

    assert (project_path / "Dockerfile").is_file()
    assert (project_path / "docker-compose.yml").is_file()
    assert (project_path / "uv.lock").is_file()


def test_invalid_project_slug_is_rejected(cookies):
    result = cookies.bake(extra_context={"project_slug": "invalid-slug"})
    assert result.exit_code != 0
