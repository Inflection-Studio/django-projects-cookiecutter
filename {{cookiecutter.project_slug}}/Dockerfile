FROM python:3.13-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    libc-dev \
    libffi-dev \
    libssl-dev \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


ARG DJANGO_SETTINGS_MODULE={{cookiecutter.project_slug}}.conf.settings.live

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} \
    POETRY_VERSION=2.4.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /code

RUN python -m pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml \
     poetry.lock \
     Makefile \
    /code/

COPY ./entrypoint.sh /code/entrypoint.sh

# make the entry point files executable
RUN chmod +x entrypoint.sh

RUN make deps-prod

COPY . .

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
