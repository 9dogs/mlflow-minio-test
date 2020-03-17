# mlflow-minio-test
Logging MLFlow artifact to MinIO storage using S3 protocol.

TLDR: run `docker-compose up`. `experiment` service fails and `patched_experiment` does not.

Test script (`mlflow_test.py`) tries to log artifact to on-premise MinIO storage using S3 protocol but without a patch 
fails with an exception:
```
botocore.exceptions.EndpointConnectionError: Could not connect to the endpoint URL: 
"http://s3.k8s00-local.amazonaws.com/mlflow-artifacts/0/69c807cb988b4eca99bccc93c9374c6f/artifacts/test_folder/test_file.txt"
```
Patched version succeeds.

MLFlow UI (http://127.0.0.1:5000/) fails with the same exception when trying to load
run info.
