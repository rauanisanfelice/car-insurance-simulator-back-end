FROM python:3.12.3 AS dependencies

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Setup the virtualenv
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install pip requirements
COPY requirements/ requirements/
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements/base.txt

WORKDIR /app
COPY /app /app

# Release
FROM python:3.12.3-bullseye AS release

# Extra python env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PATH="/venv/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/car-insurance-simulator-back-end"

# Create app directory
WORKDIR /app
COPY --from=dependencies /venv /venv
COPY . /app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.interface.api.main:app", "--reload", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--timeout", "120"]
