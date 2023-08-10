FROM python:3.10.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip

WORKDIR /NEKIDAEM_TEST

COPY poetry.lock pyproject.toml ./
RUN pip install poetry==1.5.1
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .
