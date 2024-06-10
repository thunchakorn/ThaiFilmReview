FROM python:3.11.4-slim-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y postgresql gettext

WORKDIR /app

RUN addgroup --system django \
    && adduser --system --ingroup django django

COPY --chown=django:django requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=django:django . .

RUN chown -R django:django /app

USER django
