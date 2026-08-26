# https://www.gnu.org/software/make/manual/html_node/Special-Targets.html
.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
{% if cookiecutter.use_docker == "y" %}
	@echo "  container-health-check  to check the health status of running containers"
{% endif %}
	@echo "  deps              	to install dependencies for local development"
	@echo "  deps-prod          to install dependencies for production environment"
{% if cookiecutter.use_docker == "y" %}
	@echo "  docker-deploy      builds docker containers and runs them for deployment"
	@echo "  docker-dev         builds docker containers and runs the development stack with watch"
	@echo "  docker-staging     runs the staging stack with live code mounts"
	@echo "  docker-staging-build builds images and runs the staging stack"
	@echo "  docker-down      	stop all running docker containers on the project"
{% endif %}
	@echo "  fmt-all     	   	run pre-commit hooks on all program files"
	@echo "  migrations       	make Django migrations for edited models"
	@echo "  migrate           	apply Django migrations in correct order"
	@echo "  hooks             	to update or install pre-commit hooks"
	@echo "  install-uv        	install the uv dependency manager."
	@echo "  pip-freeze  		output the contents of the pyproject.toml into a requirements.txt file"
	@echo "  show_urls			output all defined program urls on the command line"
	@echo "  test              run the automated test suite"


{% if cookiecutter.use_docker == "y" %}
CONTAINERS := {{cookiecutter.project_slug}}_django {{cookiecutter.project_slug}}_db {{cookiecutter.project_slug}}_redis {{cookiecutter.project_slug}}_web_server {{cookiecutter.project_slug}}_pg_admin
# ANSI escape codes for colors
GREEN := \033[0;32m
LIGHT_PURPLE := \033[1;35m
RESET := \033[0m
{% endif %}

PROJECT_NAME := {{cookiecutter.project_slug}}
APP_NAME :=
SETTINGS_PY := ${PROJECT_NAME}/conf/settings/common.py
APP_DIRECTORY := ${PROJECT_NAME}/apps/
APP_LABEL := login
MODEL_NAME := UserAccount
FIXTURE_NAME := users
SHELL_TYPE := ipython

# uv installation and dependency management
.PHONY: install-uv
install-uv:
	curl -LsSf https://astral.sh/uv/0.12.6/install.sh | sh

.PHONY: pip-freeze
pip-freeze:
	uv export --locked --no-dev --no-hashes --output-file requirements.txt

.PHONY: deps
deps:
	uv sync --locked

.PHONY: deps-prod
deps-prod:
	uv sync --locked --no-dev

# Django commands
.PHONY: runserver
runserver:
	uv run --locked python manage.py runserver

.PHONY: migrations
migrations:
	uv run --locked python manage.py makemigrations

.PHONY: migrate
migrate:
	uv run --locked python manage.py migrate

.PHONY: superuser
superuser:
	uv run --locked python manage.py createsuperuser

# collect static files
.PHONY: collectstatic
collectstatic:
	uv run --locked python manage.py collectstatic --noinput

.PHONY: shell
shell:
	uv run --locked python manage.py shell_plus --${SHELL_TYPE}

.PHONY: show_urls
show_urls:
	uv run --locked python manage.py show_urls

.PHONY: app
app:
	uv run --locked python manage.py startapp ${APP_NAME}
	@echo "App ${APP_NAME} created successfully"
	mv ./${APP_NAME} ${APP_DIRECTORY}
	@echo "App Moved to the apps directory ${APP_DIRECTORY}"
	@echo "Don't forget to add the app to the LOCAL_APPS apps in the settings file ${SETTINGS_PY} like so: ${PROJECT_NAME}.apps.${APP_NAME}.apps.${APP_NAME}Config"

{% if cookiecutter.use_docker == "y" %}
# Docker
.PHONY: docker-deploy
docker-deploy:
	docker compose -f docker-compose.yml up --build -d --remove-orphans

.PHONY: docker-dev
docker-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build --watch --remove-orphans

.PHONY: docker-staging
docker-staging:
	docker compose -f docker-compose.yml -f docker-compose.staging.yml up -d --remove-orphans

.PHONY: docker-staging-build
docker-staging-build:
	docker compose -f docker-compose.yml -f docker-compose.staging.yml up --build -d --remove-orphans

.PHONY: docker-down
docker-down:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down --remove-orphans

.PHONY: docker-logs
docker-logs:
	docker compose logs -f

.PHONY: container-health-check
container-health-check:
	$(foreach container,$(CONTAINERS),echo "$(GREEN)Health Check for $(container):$(RESET)" && echo "$(LIGHT_PURPLE)" && docker inspect --format '{{'{{'}}if .State.Health{{'}}'}}{{'{{'}}.State.Health.Status{{'}}'}}{{'{{'}}else{{'}}'}}{{'{{'}}.State.Status{{'}}'}}{{'{{'}}end{{'}}'}}' $(container) && echo "$(RESET)" && echo;)
{% endif %}

# Pre-commit hooks
.PHONY: hooks
hooks:
	uv run --locked pre-commit install

.PHONY: fmt-all
fmt-all:
	uv run --locked pre-commit run --all-files

# Tests
.PHONY: test
test:
	uv run --locked pytest

# Fixtures
.PHONY: dump-fixtures
dump-fixtures:
	uv run --locked python manage.py dumpdata ${APP_LABEL}.${FIXTURE_NAME} --indent 2 > fixtures/${FIXTURE_NAME}.json

.PHONY: load-fixtures
load-fixtures:
	uv run --locked python manage.py loaddata fixtures/${FIXTURE_NAME}.json --app ${APP_LABEL}.${FIXTURE_NAME}.json
