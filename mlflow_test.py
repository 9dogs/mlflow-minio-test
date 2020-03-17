import os
import time
from pathlib import Path

import mlflow

# Sleep a bit since there is a delay between MLFLow container
# start and MLFlow Server start
time.sleep(1)

mlflow.set_tracking_uri(os.environ['MLFLOW_URI'])

with mlflow.start_run():
    mlflow.log_param("alpha", 0.1)
    mlflow.log_metric("rmse", 1)
    fpath = Path('test_file.txt').resolve()
    with fpath.open('w', encoding='utf8') as f:
        f.write('Hello world!')
    mlflow.log_artifact(str(fpath), 'test_folder')
