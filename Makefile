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

lint:
	@poetry run flake8 task_manager

deploy:
	git push heroku

.PHONY: install secretkey migrate setup shell lint deploy
