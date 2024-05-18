# Use the official Python image as the base image
FROM python:3.12-slim-bookworm as python-base

# Set environment variables to non-interactive
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PDM_HOME="/opt/pdm" \
    PDM_PEP582="1" \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    PYTHONPATH="/app"

# Update PATH to include PDM and the virtual environment binaries
ENV PATH="$PDM_HOME/bin:$VENV_PATH/bin:$PATH"

# Setup the builder base with system dependencies
FROM python-base as builder-base
RUN apt-get update && apt-get install -y git curl

# Setup work directory and copy pyproject.toml (PDM uses the same pyproject.toml as Poetry)
WORKDIR $PYSETUP_PATH

# Copy dependencies
COPY ./pyproject.toml .
COPY ./pdm.lock .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel \
 && pip install --no-cache-dir pdm

# Install dependencies using PDM
RUN pdm install --check --prod --no-editable

# Setup the production environment
FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
RUN apt-get update

# Set the working directory and copy your application code
WORKDIR app/
COPY ./src /app
