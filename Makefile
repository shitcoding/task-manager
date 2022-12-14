help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | sort \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[0;32m%-30s\033[0m %s\n", $$1, $$2}'

# Environment commands
.env:  ## Creates an .env file from boilerplate .env.example file
	@test ! -f .env && cp .env.example .env

secretkey:  ## Outputs a secure secret key (i.e., for SECRET_KEY env variable)
	@poetry run python3 -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'

requirements.txt:  ## Refreshes dependencies in requirements.txt
	@poetry export --format requirements.txt --output requirements.txt --extras psycopg2 --without-hashes

# Setup
install: .env
	@poetry install --extras psycopg2-binary

migrate:  ## Run Django migrations when running app locally
	@poetry run python3 manage.py migrate

migrate-docker:  ## Run Django migrations when running app in Docker
	python3 manage.py migrate

wait-postgres:  ## Wait for postgres to start up
	python3 ./task_manager/utils/wait_for_postgres.py

setup: migrate
	@echo Create a super user:
	@poetry run python3 manage.py createsuperuser

shell:
	@poetry run python3 manage.py shell

# i18n translation commands
transprepare:
	@poetry run django-admin makemessages --ignore="static" --ignore=".venv" -a

transprepare-docker:
	django-admin makemessages --ignore="static" --ignore=".venv" -a

transcompile:
	@poetry run django-admin compilemessages --ignore="static" --ignore=".venv"

transcompile-docker:
	django-admin compilemessages --ignore="static" --ignore=".venv"

collectstatic:
	@poetry run python3 manage.py collectstatic --no-input

collectstatic-docker:
	python3 manage.py collectstatic --no-input


# Checks, tests, lint
lint:
	@poetry run flake8 task_manager

selfcheck:
	@poetry check

test:
	@export DJANGO_ALLOWED_HOSTS="*"; \
	poetry run pytest --cov=task_manager --cov-report=xml

test-coverage-report: test
	@poetry run coverage report -m $(ARGS)
	@poetry run coverage erase

test-coverage-report-xml:
	@poetry run coverage xml

check: lint selfcheck test requirements.txt

# Deployment
await-postgres:
	@./entrypoint.sh

run-dev: migrate transcompile ## Runs dev server
	@poetry run python3 manage.py runserver 0.0.0.0:8000

run-dev-docker: \
	wait-postgres \
	migrate-docker \
	transcompile-docker \
	collectstatic-docker ## Runs dev server in docker
	# python3 ./task_manager/utils/wait_for_postgres.py
	# python3 manage.py migrate
	python3 manage.py runserver 0.0.0.0:8000

run-gunicorn-dev: migrate transcompile
	@poetry run gunicorn task_manager.wsgi --bind 0.0.0.0:8000

run-gunicorn-docker: \
	wait-postgres \
	migrate-docker \
	transcompile-docker \
	collectstatic-docker ## Runs gunicorn in docker

	gunicorn task_manager.wsgi --bind 0.0.0.0:8000

deploy-heroku:	## Deploys to Heroku via git
	git push heroku

.PHONY: \
	install \
	secretkey \
	requirements.txt \
	migrate \
	setup \
	shell \
	lint \
	selfcheck \
	test \
	check \
	deploy
