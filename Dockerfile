FROM python:3.12-slim

ARG HTTP_PROXY=http://cpsp.ssi.govt.nz:8080
ARG HTTPS_PROXY=http://cpsp.ssi.govt.nz:8080
ARG NO_PROXY=localhost,127.0.0.1,ssi.govt.nz

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_TRUSTED_HOST="pypi.org pypi.python.org files.pythonhosted.org" \
    PIP_PROXY=${HTTP_PROXY} \
    HTTP_PROXY=${HTTP_PROXY} \
    HTTPS_PROXY=${HTTPS_PROXY} \
    NO_PROXY=${NO_PROXY} \
    http_proxy=${HTTP_PROXY} \
    https_proxy=${HTTPS_PROXY} \
    no_proxy=${NO_PROXY}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    unixodbc-dev \
    freetds-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH=/app

ENV HOME=/home/app
RUN mkdir -p /home/app && chmod -R 777 /home/app

COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

ENV NODE_TLS_REJECT_UNAUTHORIZED=0
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN playwright install --with-deps chromium && chmod -R a+rwX /ms-playwright

COPY . .

ENTRYPOINT ["/bin/sh", "-c", "\"$@\"; rc=$?; chmod -R a+rwX /app/allure-results 2>/dev/null; exit $rc", "entrypoint"]
CMD ["pytest", "-ra", "--disable-pytest-warnings", "--capture=no", "--color=no"]

# Build
# docker build -t integration-tests .

# Navigate to the project folder and run command
# docker run --rm  -v "${PWD}:/app" integration-tests:latest pytest ./tests/api_test/soap_api/comparison_testing/steps_def/ -n auto
