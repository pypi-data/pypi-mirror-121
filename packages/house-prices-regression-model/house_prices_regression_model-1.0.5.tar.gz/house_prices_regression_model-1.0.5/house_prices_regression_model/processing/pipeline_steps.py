# Imports
from sklearn.base import BaseEstimator, TransformerMixin

#Module import
from house_prices_regression_model.config.core import load_config_file,SETTINGS_PATH

# Config file
config = load_config_file(SETTINGS_PATH)
VARS_MODELO = config["VARS_MODELO"]

#####################IMPUTING MISSING VALUES############
class MissingImputing(BaseEstimator, TransformerMixin):
    def __init__(self):
        return None

    def fit(self, df, y=None):
        # Nothing to do here, just return the dataframe as is
        return self

    def transform(self, df):
        df = df.copy()
        df = df.fillna(0)
        return df


######################SELECT VARIABLES###################
class SelectVariables(BaseEstimator, TransformerMixin):
    def __init__(self):
        return None

    def fit(self, df, y=None):
        # Nothing to do here, just return the dataframe as is
        return self

    def transform(self, df):
        df = df.copy()
        df = df[VARS_MODELO]
        return df