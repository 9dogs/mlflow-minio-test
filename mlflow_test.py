import os
import time
from pathlib import Path

import mlflow

# Sleep a bit since there is a delay between MLFLow container
# start and MLFlow Server start
time.sleep(1)

mlflow.set_tracking_uri(os.environ['MLFLOW_URI'])

if os.environ.get('ENABLE_PATCH'):
    from mlflow.store.artifact.s3_artifact_repo import S3ArtifactRepository
    def _get_s3_client(self):
        import boto3
        s3_endpoint_url = os.environ.get('MLFLOW_S3_ENDPOINT_URL')
        s3_region_name = os.environ.get('MLFLOW_S3_REGION_NAME')
        return boto3.client(
            's3', endpoint_url=s3_endpoint_url, region_name=s3_region_name
        )
    S3ArtifactRepository._get_s3_client = _get_s3_client

with mlflow.start_run():
    mlflow.log_param("alpha", 0.1)
    mlflow.log_metric("rmse", 1)
    fpath = Path('test_file.txt').resolve()
    with fpath.open('w', encoding='utf8') as f:
        f.write('Hello world!')
    mlflow.log_artifact(str(fpath), 'test_folder')
