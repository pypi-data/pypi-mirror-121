#Imports
import pandas as pd
from sklearn.pipeline import Pipeline
import typing as t
import joblib
from house_prices_regression_model import __version__ as VERSION
from house_prices_regression_model.config.core import load_config_file
from house_prices_regression_model.config.core import TRAINED_MODEL_DIR, SETTINGS_PATH

# Config file
config = load_config_file(SETTINGS_PATH)
PIPELINE_ARTIFACT_NAME = config["PIPELINE_ARTIFACT_NAME"]


#Load dataset
def load_dataset(*, data_path: str) -> pd.DataFrame:
    df = pd.read_csv(data_path)
    return df

#Remove old pipelines
def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()

#Persist the artifact .pkl created by the pipeline
def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    save_file_name = f"{PIPELINE_ARTIFACT_NAME}_v{VERSION}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)

#Load an already persisted pipeline
def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""
    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


