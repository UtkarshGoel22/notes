#!/bin/bash

# Create virtual environment
if test -d "$(pwd)/venv";
    then
    echo "Virtual environment - venv already exists"
    source venv/bin/activate
else
    echo "Creating virtual environment"
    virtualenv --python=python3.10 venv
    source venv/bin/activate
fi

# Install requirements
PIPFILE="$(pwd)/Pipfile"

pip show pipenv

if [ $? -eq 0 ]
then
  echo "Success: pipenv was found"
else
  echo "Failure: pipenv not found. Installing pipenv now" >&2
  pip install pipenv
fi

if test -f "$PIPFILE";
    then
    echo "Installing dev requirements"
    pipenv install --dev
else
    echo "Pipfile does not exist!"
fi
