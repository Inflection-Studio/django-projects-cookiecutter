# https://www.gnu.org/software/make/manual/html_node/Special-Targets.html
.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  container-health-check  to check the health status of running containers"
	@echo "  deps              	to install dependencies for local development"
	@echo "  deps-prod          to install dependencies for production environment"
	@echo "  docker-deploy      builds docker containers and runs them for deployment"
	@echo "  docker-down      	stop all running docker containers on the project"
	@echo "  fmt-all     	   	run pre-commit hooks on all program files"
	@echo "  makemigrations    	make Django makemigrations for edited models"
	@echo "  migrate           	apply Django migrations in correct order"
	@echo "  hooks             	to update or install pre-commit hooks"
	@echo "  install-poetry    	install poetry dependency manager."
	@echo "  uninstall-poetry  	uninstalls poetry if things go wrong."
	@echo "  pip-freeze  		output the contents of the pyproject.toml into a requirements.txt file"
	@echo "  show_urls			output all defined program urls on the command line"


CONTAINERS := {{cookiecutter.project_slug}}_db {{cookiecutter.project_slug}}_web_server {{cookiecutter.project_slug}}_pg_admin
# ANSI escape codes for colors
GREEN := \033[0;32m
LIGHT_PURPLE := \033[1;35m
RESET := \033[0m

PROJECT_NAME := {{cookiecutter.project_slug}}
APP_NAME :=
SETTINGS_PY := ${PROJECT_NAME}/conf/settings/common.py
APP_DIRECTORY := ${PROJECT_NAME}/apps/
APP_LABEL := login
MODEL_NAME := UserAccount
FIXTURE_NAME := users
SHELL_TYPE := ipython

# poetry installation
.PHONY: install-poetry
install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: uninstall-poetry
uninstall-poetry:
	curl -sSL https://install.python-poetry.org | python3 - --uninstall

# poetry dependency management
.PHONY: pip-freeze
pip-freeze:
	pip --disable-pip-version-check list --format=freeze > requirements.txt

.PHONY: deps-clean
deps-clean:
	poetry env use 3.13.0

.PHONY: deps
deps: deps-clean
	poetry install --no-cache

.PHONY: deps-prod
deps-prod:
	poetry config virtualenvs.create false
	poetry install --no-interaction --no-ansi --without dev

# Django commands
.PHONY: runserver
runserver: deps-clean
	poetry run python manage.py runserver

.PHONY: migrations
migrations: deps-clean
	poetry run python manage.py makemigrations

.PHONY: migrate
migrate: deps-clean
	poetry run python manage.py migrate

.PHONY: superuser
superuser: deps-clean
	poetry run python manage.py createsuperuser

# collect static files
.PHONY: collectstatic
collectstatic: deps-clean
	poetry run python manage.py collectstatic --noinput

.phony: shell
shell: deps-clean
	poetry run python manage.py shell_plus --${SHELL_TYPE}

.PHONY: show_urls
show_urls: deps-clean
	poetry run python manage.py show_urls

.phony: app
app:
	poetry run python manage.py startapp ${APP_NAME}
	@echo "App ${APP_NAME} created successfully"
	mv ./${APP_NAME} ${APP_DIRECTORY}
	@echo "App Moved to the apps directory ${APP_DIRECTORY}"
	@echo "Don't forget to add the app to the LOCAL_APPS apps in the settings file ${SETTINGS_PY} like so: ${PROJECT_NAME}.apps.${APP_NAME}.apps.${APP_NAME}Config"

# docker
.PHONY: docker-deploy
docker-deploy:
	docker compose up --build -d --remove-orphans

.PHONY: docker-down
docker-down:
	docker compose down --remove-orphans

.PHONY: docker-logs
docker-logs:
	docker compose logs -f

.PHONY: container-health-check
container-health-check:
	$(foreach container,$(CONTAINERS),echo "$(GREEN)Health Check for $(container):$(RESET)" && echo "$(LIGHT_PURPLE)" && docker inspect' $(container) && echo "$(RESET)" && echo)

# Pre-commit hooks
.PHONY: hooks
hooks:
	hooks-init
	pre-commit install

.PHONY: fmt-all
fmt-all:
	pre-commit run --all-files

# Fixtures
.PHONY: dump-fixtures
dump-fixtures:
	poetry run python manage.py dumpdata ${APP_LABEL}.${FIXTURE_NAME} --indent 2 > fixtures/${FIXTURE_NAME}.json

.PHONY: load-fixtures
load-fixtures:
	poetry run python manage.py loaddata fixtures/${FIXTURE_NAME}.json --app ${APP_LABEL}.${FIXTURE_NAME}.json
