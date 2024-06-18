FROM python:3.11.7-alpine3.19

WORKDIR /opt

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

COPY ./ /opt

RUN pip install --no-cache-dir -r /opt/requirements.txt