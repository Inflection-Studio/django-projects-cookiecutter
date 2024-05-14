# Platform

> Main Repository for Backend Web App and API for platform

1. [Requirements](#requirements)
2. [Setup](#setup)
3. [Usage](#usage)
4. [Development](#development)

## Requirements

**This project uses Docker Compose to manage multiple services.
Make sure you have Docker and Docker Compose installed on your machine.**

1. Python 3.12.0 installed
2. Text editor such as [vs code](https://code.visualstudio.com/) or sublime text
3. Git - preferrably use terminal like [gitbash](https://gitforwindows.org/)
4. Poetry dependency manager - See setup instructions [here](https://python-poetry.org/docs/)

## Setup

1. Clone the repository.
2. Change directory to the location of this repository.
3. Create a `.env` file using the included `.env.example` as an example.
4. Generate a secret key for your app and paste into the SECRET_KEY section of .env file
you can find generate the key from [here](https://djecrety.ir/)
5. Create and start your preferred Python virtual environment. For
more information on how to set up a virtual environment, check the instructions on [this link](https://tutorial.djangogirls.org/en/django_installation/). Install the required libraries by running the commands below, by changing to
the project directory.

        make deps

6. After installation, run the following command:

       make migrate

7. A local ```dbsqlite``` file will be generate at the root of the project.
8. Create a superuser by running the ``make superuser`` and fill in the details.
9. After creating superuser run ``make runserver`` open the browser and run  ``127.0.0.1:8000/admin`` , login with the credentials created.
10. For details of how to get started with django, check out [this link](https://www.djangoproject.com/start/)
11. In order to work with a virtual environment, check out [this link](https://tutorial.djangogirls.org/en/installation/#pythonanywhere)

## Usage

To run locally:

    make runserver

## Development

Ensure you have t installed globally by running `pre-commit install` for pre-commit hooks to run.

Pull the latest main version:

    git pull origin main

Create local development branch and switch to it:

    git branch {feature_branch_name}
    git checkout {feature_branch_name}

Make desired changes then commit the branch.

    git add .
    git commit -m "changes to{feature_branch_name}"
    git push origin {feature_branch_name}

**If using poetry for dependency management, you can pip freeze them to a `requirements.txt` file by running**

    pip --disable-pip-version-check list --format=freeze > requirements.txt

### Creating an App

To create a new Django app, run the following command

    make app APP_NAME={app_name}

Add the newly created app to the list of `INSTALLED_APPS` on the `{{cookiecutter.project_slug}}.conf.settings.common.py` file
under the `LOCAL_APPS_LIST`

    LOCAL_APPS = [
        "{{cookiecutter.project_slug}}.apps.{app_name}.apps.{AppName}Config",
    ]

### Running Health Checks

Health checks have been configured for each service to ensure they are running and ready to accept connections.

1. Nginx Services

    docker inspect --format='{{json .State.Health}}' {{cookiecutter.project_slug}}_web_server

2. Postgres Service

    docker inspect --format='{{json .State.Health}}' {{cookiecutter.project_slug}}_db
