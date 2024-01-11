FROM python:3.10.0-slim
ARG ENV

# install dependencies
WORKDIR /tmp
COPY linux-packages.txt linux-packages.txt
RUN apt-get update && \
  apt-get install -yq --no-install-recommends \
  $(grep -vE '^#' linux-packages.txt) && \
  rm -rf /var/lib/apt/lists/* && \
  pip install poetry

WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry config virtualenvs.create false \
    && poetry install $(if [ "$ENV" = "TEST" ]; then echo "--all-extras" ; else echo "--no-dev"; fi) --no-interaction --no-ansi --no-root

COPY . .
