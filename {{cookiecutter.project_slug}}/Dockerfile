FROM python:3.13-slim AS base

ARG DJANGO_SETTINGS_MODULE={{cookiecutter.project_slug}}.conf.settings.live

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}

WORKDIR /code


FROM base AS builder

ARG POETRY_VERSION=2.4.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    libc-dev \
    libffi-dev \
    libssl-dev \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir "poetry==${POETRY_VERSION}" \
    && python -m venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --no-root --only main


FROM base AS runtime

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
