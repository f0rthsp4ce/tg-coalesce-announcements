# syntax=docker/dockerfile:1
FROM python:3.11-slim as base

# https://github.com/michaeloliverx/python-poetry-docker-example/blob/f7241bf6586e99c6c649eba36ca0efd935ea6316/docker/Dockerfile#L6
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev

# Fixup venv for distroless
RUN ln -fs /usr/bin/python .venv/bin/python

FROM gcr.io/distroless/python3-debian12 AS runtime
WORKDIR /app

COPY --from=base /app/.venv ./.venv
COPY ./app ./app
COPY settings.json ./.

ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["python", "app/__init__.py", "monitor"]