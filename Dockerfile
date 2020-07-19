FROM python:3.7.5-slim-buster

RUN apt-get update && apt-get -y install --no-install-recommends \
        build-essential \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
# Install MLFlow
RUN pip install \
    psycopg2-binary \
    mlflow \
    boto3

EXPOSE 5000

CMD mlflow server \
  --backend-store-uri ${BACKEND_URI} \
  --default-artifact-root ${ARTIFACT_ROOT} \
  --host 0.0.0.0
