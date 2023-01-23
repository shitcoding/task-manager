#### Build stage ####
FROM python:3.10-alpine as builder

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install psycopg2 dependencies
RUN apk update && apk add \
  postgresql-dev \
  gcc \
  python3-dev \
  musl-dev \
  curl

# Install poetry and create requirements.txt
RUN pip install --upgrade pip
RUN pip install poetry
COPY . .
# RUN poetry export --format requirements.txt --output requirements.txt --extras psycopg2 --without-hashes

# Export without dev dependencies for staging and production builds
RUN sh -c 'if [ "$MODE" = 'staging' ] || [ "$MODE" = 'production' ]; then poetry export --format requirements.txt --output requirements.txt --without dev --extras psycopg2 --without-hashes; fi'
# Export with dev dependencies for development builds
RUN sh -c 'if [ "$MODE" = 'dev' ]; then poetry export --format requirements.txt --output requirements.txt --with dev --extras psycopg2 --without-hashes; fi'

# Create wheels
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#### Final stage ####
FROM python:3.10-alpine

# Create directory for the app user
RUN mkdir -p /home/app

# Create non-root app user
RUN addgroup -S app && adduser -S app -G app

# Create appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# Install dependencies
RUN apk update && apk add \
  libpq \
  make \
  gettext
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy project
COPY . $APP_HOME

# Chown all files to the app user
RUN chown -R app:app $APP_HOME

# Change to the app user
USER app
