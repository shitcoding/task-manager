help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | sort \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[0;32m%-30s\033[0m %s\n", $$1, $$2}'

# Environment commands
# ------------------------------------------------------------------------------
env-dev:  ## Create template .env files for dev environment (if files don't exist already)
	@test ! -f ./.envs/.dev/.db && cp ./.envs/.dev/.db.example ./.envs/.dev/.db
	@test ! -f ./.envs/.dev/.django && cp ./.envs/.dev/.django.example ./.envs/.dev/.django

env-staging:  ## Create template .env files for staging environment (if files don't exist already)
	@test ! -f ./.envs/.staging/.db && cp ./.envs/.staging/.db.example ./.envs/.staging/.db
	@test ! -f ./.envs/.staging/.django && cp ./.envs/.staging/.django.example ./.envs/.staging/.django
	@test ! -f ./.envs/.staging/.nginx-proxy-letsencrypt && \
		cp ./.envs/.staging/.nginx-proxy-letsencrypt.example ./.envs/.staging/.nginx-proxy-letsencrypt

env-production:  ## Create template .env files for production environment (if files don't exist already)
	@test ! -f ./.envs/.production/.db && cp ./.envs/.production/.db.example ./.envs/.production/.db
	@test ! -f ./.envs/.production/.django && cp ./.envs/.production/.django.example ./.envs/.production/.django
	@test ! -f ./.envs/.production/.nginx-proxy-letsencrypt && \
		cp ./.envs/.production/.nginx-proxy-letsencrypt.example ./.envs/.production/.nginx-proxy-letsencrypt

env-all: env-dev env-staging env-production  ## Create .env files for all environments: dev, staging, production (if files don't exist already)

secretkey:  ## Output a secure secret key (i.e. for using as Django SECRET_KEY env variable)
	@poetry run python3 -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'

requirements:  ## Refresh app dependencies in requirements.txt
	@poetry export --format requirements.txt --output requirements.txt --extras psycopg2 --without-hashes


# App setup
# ------------------------------------------------------------------------------
migrate:  ## Run database migrations (when running app locally)
	@poetry run python3 manage.py migrate

migrate-docker:  ## Run database migrations (when running app in Docker)
	python3 manage.py migrate

wait-postgres:  # Wait for postgres to start up
	python3 ./task_manager/utils/wait_for_postgres.py

install: .env
	@poetry install --extras psycopg2-binary

setup: migrate
	@echo Create a super user:
	@poetry run python3 manage.py createsuperuser

shell:  ## Run Django REPL shell
	@poetry run python3 manage.py shell


# i18n localization/translation commands
# ------------------------------------------------------------------------------
transprepare:
	@poetry run django-admin makemessages --ignore="static" --ignore=".venv" -a

transprepare-docker:
	django-admin makemessages --ignore="static" --ignore=".venv" -a

transcompile:
	@poetry run django-admin compilemessages --ignore="static" --ignore=".venv"

transcompile-docker:
	django-admin compilemessages --ignore="static" --ignore=".venv"


# Static files management
# ------------------------------------------------------------------------------
collectstatic:  # Run Django migrations (when running app locally) 
	@poetry run python3 manage.py collectstatic --no-input

collectstatic-docker:  # Run Django migrations (when running app in Docker)
	python3 manage.py collectstatic --no-input


# Checks, tests, lint
lint:  ## Run flake8 code linter
	@poetry run flake8 task_manager

selfcheck:
	@poetry check

test:  ## Run tests
	@export DJANGO_ALLOWED_HOSTS="*"; \
	poetry run pytest --cov=task_manager --cov-report=xml

test-coverage-report: test
	@poetry run coverage report -m $(ARGS)
	@poetry run coverage erase

test-coverage-report-xml:
	@poetry run coverage xml

check: lint selfcheck test requirements.txt

# App deployment
# ------------------------------------------------------------------------------
run-dev: migrate transcompile  ## Run Django dev server (when running app locally)
	@poetry run python3 manage.py runserver 0.0.0.0:8000

run-dev-docker: \
	wait-postgres \
	migrate-docker \
	transcompile-docker \
	collectstatic-docker  ## Run Django dev server (when running app in Docker)

	python3 manage.py runserver 0.0.0.0:8000

run-gunicorn-dev: migrate transcompile
	@poetry run gunicorn task_manager.wsgi --bind 0.0.0.0:8000

run-gunicorn-docker: \
	wait-postgres \
	migrate-docker \
	transcompile-docker \
	collectstatic-docker  ## Run gunicorn wsgi server (when running app in Docker)

	gunicorn task_manager.wsgi --bind 0.0.0.0:8000

deploy-heroku:	## Deploy the app to Heroku via git
	git push heroku


.PHONY: \
	help \
	env-dev \
	env-staging \
	env-production \
	env-all \
	secretkey \
	requirements \
	migrate \
	migrate-docker \
	wait-postgres \
	install \
	setup \
	shell \
	transprepare \
	transprepare-docker \
	transcompile \
	transcompile-docker \
	collectstatic \
	collectstatic-docker \
	lint \
	selfcheck \
	test \
	test-coverage-report \
	test-coverage-report-xml \
	check \
	run-dev \
	run-dev-docker \
	run-gunicorn-dev \
	run-gunicorn-docker \
	deploy-heroku
