FROM python:3.10-alpine
ARG APP_NAME=task_manager
ARG APP_PATH=/opt/$APP_NAME

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=false \
  PATH=/home/user/.local/bin:$PATH

ENV POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true

RUN apk add \
  gettext \
  git \
  make \
  postgresql-dev \
  curl

RUN curl -sSL https://install.python-poetry.org/ | python
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR $APP_PATH

RUN adduser -D user \
  && chown -R user:user ./

USER user

COPY --chown=user:user ./ ./
RUN poetry install --only main --extras psycopg2-binary

ENV SECRET_KEY=$("make secretkey")

CMD ["make", "start"]
