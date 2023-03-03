#### Build stage ####
FROM python:3.10-alpine as builder

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up build mode (dev, staging or production)
ARG BUILD_MODE
ENV MODE=${BUILD_MODE}

# Install psycopg2 dependencies
RUN apk update && apk add \
  postgresql-dev \
  gcc \
  python3-dev \
  musl-dev \
  curl \
  make

# Install poetry and create requirements.txt
RUN pip install --upgrade pip
RUN pip install poetry
COPY . .
# Export dependencies to requirements.txt:
# with dev dependencies if MODE=dev,
# without dev dependencies if MODE=staging or production
RUN make reqs


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
