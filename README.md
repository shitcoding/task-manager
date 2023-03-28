[![Python CI](https://github.com/shitcoding/python-project-lvl4/actions/workflows/CI.yml/badge.svg)](https://github.com/shitcoding/python-project-lvl4/actions/workflows/CI.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/49e3fce0533f78da6b43/maintainability)](https://codeclimate.com/github/shitcoding/python-project-lvl4/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/49e3fce0533f78da6b43/test_coverage)](https://codeclimate.com/github/shitcoding/python-project-lvl4/test_coverage)
---
# Task manager with Django backend

Task manager app similar to [Redmine](http://redmine.org).

Features:
- User signup, authentication, authorization
- Creation of tasks, task statuses, labels, assigning performers
- i18n localization/internationalization

## Tech stack:
- Backend: Django, gunicorn, Postgres
- Frontend: Bootstrap + `django-crispy-forms` + a bit of custom CSS
- Deployment:
  - Dockerized, with separate `docker-compose` files for running in dev, staging, production environments
  - `Procfile` for deploying to Heroku
  - Static files served with nginx acting like a reverse proxy with [`nginx-proxy`](https://github.com/nginx-proxy/nginx-proxy) and [`letsencrypt-nginx-proxy-companion`](https://github.com/nginx-proxy/docker-letsencrypt-nginx-proxy-companion) used to issue and renew SSL certificates
- Tests, CI/CD:
  - `pytest`
  - Github Actions


---
## Installing and running the app
1. Install [Docker](https://www.docker.com/get-started)

2. Clone the repo and `cd` into the project directory:
```sh
git clone https://github.com/shitcoding/task-manager
cd task-manager
```

3. Create environment files with credentials for Django, Postgres, Let's Encrypt
Environment files are stored in `.envs/` directory in the root of the project, with separate subdirectories for dev, staging and production environments.

3.1. Run the following commands to create environment files from template .env.example files:
```sh
# Create .env files for dev environment (if files don't exist already)
make env-dev
# Create .env files for staging environment (if files don't exist already)
make env-staging
# Create .env files for production environment (if files don't exist already)
make env-production
# Create .env files for all environments: dev, staging, production (if files don't exist already)
make env-all
```

3.2. Enter credentials to the newly created .env files.

> **IMPORTANT!** Change the credentials in the created `.env` files!
> If you don't do it, your website will be totally insecure and/or won't work at all.

For example, for production environment:
```sh
# ./envs/.production/.django
# ------------------------------------------------------------------------------
# Production environment Django app settings and credentials
# ------------------------------------------------------------------------------
# General
MODE=production
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=WowSoSecret # Change the value
DJANGO_ALLOWED_HOSTS=.yourdomain.com # Enter your domain name with leading dot
```
```sh
# ./envs/.production/.db
# ------------------------------------------------------------------------------
# Production environment database settings
# ------------------------------------------------------------------------------
# PostgreSQL credentials
POSTGRES_DB=task_manager_db # Change the value
POSTGRES_USER=task_manager_user # Change the value
POSTGRES_PASSWORD=task_manager_password # Change the value
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Uncomment this line and comment out postgres settings
# in order to use managed database like AWS RDS:
# DATABASE_URL=psql://<user>:<password>@<host>:<port>/<db_name>
```
```sh
# ./envs/.production/.nginx-proxy-letsencrypt
# ------------------------------------------------------------------------------
# letsencrypt-nginx-proxy-companion credentials
# https://github.com/jwilder/docker-letsencrypt-nginx-proxy-companion
# ------------------------------------------------------------------------------
# Letsencrypt settings
DEFAULT_EMAIL=mail@yourdomain.com # Enter email to use for Letsencrypt CA
VIRTUAL_HOST=yourdomain.com # Enter your domain name
VIRTUAL_PORT=8000
LETSENCRYPT_HOST=yourdomain.com # Enter your domain name
```



4. Run `docker-compose` for the environment you need (development, staging or production) to start the app containter and other required services (postgres, nginx, etc.)

#### To run the Docker container with development environment:
```sh
make docker-up-dev
# Or:
docker-compose -f docker-compose.dev.yml up -d --build
```
This will start the application containter in development mode on http://127.0.0.1:8000/ together with postgres database containter.

#### To run the Docker container with staging environment:
```sh
make docker-up-staging
# Or:
docker-compose -f docker-compose.staging.yml up -d --build
```

#### To run the Docker container with production environment:
```sh
make docker-up-production
# Or:
docker-compose -f docker-compose.production.yml up -d --build
```

In case of staging and production environments, we start Django app containter, Postgres database, [`nginx-proxy`](https://github.com/nginx-proxy/nginx-proxy) and [`letsencrypt-nginx-proxy-companion`](https://github.com/nginx-proxy/docker-letsencrypt-nginx-proxy-companion) containers.
  - nginx-proxy - used to automatically build your Nginx proxy configuration for running containers where each container is treated as a single virtual host
  - letsencrypt-nginx-proxy-companion - used to issue and renew Let's Encrypt SSL certificates for each of the containers proxied by nginx-proxy

The difference between staging and production environments is using either [Let's Encrypt's staging environment](https://letsencrypt.org/docs/staging-environment/) or its' production environment, as Let's Encrypt enforces [rate limitations](https://letsencrypt.org/docs/rate-limits/) on their production validation system:
  - 5 validation failures per account, per hostname, per hour
  - 50 certificates may be created per domain per week


#### Generating dummy content for task manager

To generate dummy content (tasks, users, labels, statuses) automatically, use custom Django management command:
```sh
# Generate 10 dummy tasks along with creator/performer users, task labels, statuses
python3 manage.py create_dummy_content
# Or use --num-tasks argument to generate the specific amount of tasks
python3 manage.py create_dummy_content --num-tasks=1337
```


---
## Tests and code quality
App uses the following tools:
- `pytest` for unit tests
- `flake8` as the linter
- `pytest-cov` and `coverage` to check code coverage

Github Actions workflow runs tests, linter and code coverage check automatically.
In order to run them manually, use the following commands:
```sh
# Run tests
make test

# Run flake8 code linter
make lint

# Run code coverage check
make test-coverage-report

# Run all the checks above
make check
```

---
