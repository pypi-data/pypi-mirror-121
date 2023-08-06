from pathlib import Path
import yaml

# Reading from config file
def load_config_file(config_file):
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config

PACKAGE_ROOT = Path(__file__).resolve().parent.parent #house_prices_regression_model
ROOT = PACKAGE_ROOT.parent  #Package_deployment
DATASET_DIR = PACKAGE_ROOT / "dat"
FILE_NAME_DATA_TRAIN = "train.csv"
FILE_NAME_DATA_TEST = "test.csv"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
SETTINGS_PATH = PACKAGE_ROOT / "config" / "settings.yml"