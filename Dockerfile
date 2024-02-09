FROM python:3.12-bullseye as builder

WORKDIR /opt/weatherapp

ENV \
PIP_DISABLE_PIP_VERSION_CHECK="1" \
PIP_NO_CACHE_DIR="1"

RUN pip install poetry==1.7.0

ENV \
POETRY_NO_INTERACTION="1" \
POETRY_VIRTUALENVS_IN_PROJECT="1" \
POETRY_VIRTUALENVS_CREATE="1" \
POETRY_CACHE_DIR="/tmp/.poetry"

COPY poetry.lock pyproject.toml .
RUN \
--mount=type=cache,target=$POETRY_CACHE_DIR \
poetry install --only=main --no-interaction --no-ansi


FROM python:3.12-slim-bullseye as runtime

WORKDIR /opt/weatherapp

ENV \
PATH="/opt/weatherapp/.venv/bin:$PATH" \
PYTHONPATH="${PYTHONPATH}:/opt/weatherapp"

COPY --from=builder /opt/weatherapp/.venv .venv
COPY weatherapp .

CMD ["gunicorn", "core.wsgi", "-b", "0.0.0.0:8000", "-w", "1"]