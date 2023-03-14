FROM python:3.11 AS dev_build

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.3.1 \
  POETRY_CACHE_DIR="/var/cache/pypoetry" \
  PATH="$PATH:/root/.local/bin"

RUN apt update \
  # Installing `poetry` package manager:
  # https://github.com/python-poetry/poetry
  && curl -sSL https://install.python-poetry.org | python3 -
RUN poetry --version \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /root/services/task_admin
COPY ./libraries/rmq_broker /root/libraries/rmq_broker
COPY ./services/task_admin /root/services/task_admin

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi -vvv \
  && rm -rf $POETRY_CACHE_DIR


ENV ADMIN_PASSWORD="admin-password-1234" \
    DATABASE_URL="postgresql://postgres:postgrespw@postgres-k3zM:5432/task-admin"

CMD ["poetry", "run", "uvicorn", "task_admin.app:app", "--host", "0.0.0.0", "--port", "8000"]