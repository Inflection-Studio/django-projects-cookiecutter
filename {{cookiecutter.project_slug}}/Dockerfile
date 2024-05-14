FROM python:3.12.0

ARG GIT_SHA
ARG DJANGO_SETTINGS_MODULE=projectBaseline.conf.settings.live

ENV PYTHONUNBUFFERED 1 \
    GIT_SHA=${GIT_SHA:-} \
    DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
# RUN mkdir /code

WORKDIR /code
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
COPY pyproject.toml \
     poetry.lock \
     Makefile \
    /code/

# Upgrade pip to the latest version to stop any error messages
RUN python3 -m pip install -U pip

# install poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.8.3

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY ./entrypoint.sh /code/entrypoint.sh

# make the entry point files executable
RUN chmod +x entrypoint.sh

COPY . .

RUN make deps-prod

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
