install: .env
	@poetry install --extras psycopg2-binary

.env:
	@test ! -f .env && cp .env.example .env

secretkey:
	@poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'

requirements.txt:
	@poetry export --format requirements.txt --output requirements.txt --extras psycopg2 --without-hashes

migrate:
	@poetry run python manage.py migrate

setup: migrate
	@echo Create a super user:
	@poetry run python manage.py createsuperuser

shell:
	@poetry run python manage.py shell

# Need to have GNU gettext installed
transprepare:
	@poetry run django-admin makemessages --ignore="static" --ignore=".venv" -a

transcompile:
	@poetry run django-admin compilemessages --ignore="static" --ignore=".venv"

collectstatic:
	@poetry run python manage.py collectstatic --no-input

lint:
	@poetry run flake8 task_manager

selfcheck:
	@poetry check

test:
	@poetry run pytest

test-coverage-report: test
	@poetry run coverage report -m $(ARGS)
	@poetry run coverage erase

test-coverage-report-xml:
	@poetry run coverage xml

check: lint selfcheck test requirements.txt

deploy:
	git push heroku

start: migrate transcompile
	@poetry run gunicorn task_manager.wsgi --bind 0.0.0.0:$(PORT)
	# poetry run python3 manage.py runserver 0.0.0.0:$(PORT)

.PHONY: install secretkey requirements.txt migrate setup shell lint selfcheck test check deploy
