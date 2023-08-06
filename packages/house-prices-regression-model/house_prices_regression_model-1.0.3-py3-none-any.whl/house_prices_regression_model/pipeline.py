###############Libraries###############
from catboost import CatBoostRegressor
from sklearn.pipeline import Pipeline
from feature_engine.transformation import LogTransformer

#Module imports
from house_prices_regression_model.processing.pipeline_steps import MissingImputing, SelectVariables
from house_prices_regression_model.config.core import load_config_file,SETTINGS_PATH

# Config file
config = load_config_file(SETTINGS_PATH)
VARS_NUM_LOG = config["VARS_NUM_LOG"]

# MODELO#
random_state = 24
dict_best_params = {'learning_rate': 0.1, 'max_depth': 4, 'n_estimators': 200, 'subsample': 0.85, 'loss_function': 'RMSE'}
cb_model = CatBoostRegressor(**dict_best_params, random_state=random_state, verbose=False)

######################PIPELINE#####################################
cb_pipe = Pipeline([
    # ===== IMPUTATION =====
    ('imputing_missing', MissingImputing()),

    # ==== VARIABLE SELECTION =====
    ('select_variables', SelectVariables()),

    # ==== VARIABLE TRANSFORMATION =====
    ('log', LogTransformer(variables=VARS_NUM_LOG)),

    # ==== MODEL TRAINING =====
    ('cb', cb_model)

])