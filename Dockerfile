# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Install pipenv
RUN pip install pipenv==2023.12.1

# Copy application dependency manifests to the container image.
# Copying this separately prevents re-running pip install on every code change (Layer gets cached).
COPY Pipfile .
COPY Pipfile.lock .
# Install dependencies.
RUN pipenv install --dev --system

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

EXPOSE $PORT

CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 --timeout 0 app:app
