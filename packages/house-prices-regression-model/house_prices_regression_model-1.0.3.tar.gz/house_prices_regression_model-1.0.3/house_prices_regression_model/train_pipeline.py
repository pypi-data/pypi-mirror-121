#Imports
import numpy as np
from pathlib import Path

#Module imports
from house_prices_regression_model.pipeline import cb_pipe
from house_prices_regression_model.config.core import load_config_file, DATASET_DIR, FILE_NAME_DATA_TRAIN, SETTINGS_PATH
from house_prices_regression_model.processing.data_manager import load_dataset, save_pipeline

# Config file
config = load_config_file(SETTINGS_PATH)
TARGET = config["TARGET"]
VARS_CAT = config["VARS_CAT"]
TRAIN_DATA_PATH = Path(f"{DATASET_DIR}/{FILE_NAME_DATA_TRAIN}")


#Run training
def run_training() -> None:
    """Train the model."""

    # read training data
    df = load_dataset(data_path=TRAIN_DATA_PATH)
    df[TARGET] = np.log(df[TARGET])

    # fit model
    cb_params_fit = {'cb__cat_features': VARS_CAT}
    cb_pipe.fit(X=df,
                y=df[TARGET],
                **cb_params_fit)

    # persist trained model
    save_pipeline(pipeline_to_persist=cb_pipe)

if __name__ == "__main__":
    run_training()