import logging
import os
import time
from pathlib import Path
from tempfile import TemporaryDirectory

import boto3
import mlflow
from mlflow.data import parse_s3_uri
from mlflow.entities import Run

logger = logging.getLogger(__name__)


def ensure_s3_bucket_for_run(run: Run):
    """Create bucket if not exists.

    :param run: MLFlow run
    """
    try:
        bucket, __ = parse_s3_uri(run.info.artifact_uri)
    except Exception:
        pass
    else:
        s3_endpoint_url = os.environ.get("MLFLOW_S3_ENDPOINT_URL")
        if s3_endpoint_url:
            s3_client = boto3.client("s3", endpoint_url=s3_endpoint_url)
            try:
                s3_client.create_bucket(Bucket=bucket)
            except (
                s3_client.exceptions.BucketAlreadyExists,
                s3_client.exceptions.BucketAlreadyOwnedByYou,
            ):
                logger.info("Bucket already exists", bucket=bucket)


# Sleep a bit since there is a delay between MLFLow container
# start and MLFlow Server start
time.sleep(1)

mlflow.set_tracking_uri(os.environ["MLFLOW_URI"])


with mlflow.start_run() as run:
    mlflow.log_param("alpha", 0.1)
    mlflow.log_metric("rmse", 1)
    fpath = Path("test_file.txt").resolve()
    ensure_s3_bucket_for_run(run)
    with TemporaryDirectory() as tmp_dir:
        test_file_path = Path(tmp_dir) / "test_file.txt"
        with test_file_path.open("w") as f:
            f.write("Hello world!")
        mlflow.log_artifact(str(test_file_path))
