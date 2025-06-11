import logging

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import max_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
#from src.mca.catalog import catalog

def values_counts_damage_type(data:pd.DataFrame):
    list_features = []
    for d in data:

        damage_types = []
        for ability in ["Q", "W", "E", "R", "passive"]:
            damage_types.extend(d[ability]["damage"])
    
        list_features.extend([x for x in damage_types if x is not None])
    df = get_value_counts(list_features,"damage_type")
    return df

def values_counts_modifier_name(data:pd.DataFrame):
    list_features = []
    for d in data:

        modifier_list = []
        for ability in ["Q", "W", "E", "R", "passive"]:
            modifier_list.extend(d[ability]["effects"])
    
        list_features.extend([x for x in modifier_list if x is not None])
    df = get_value_counts(list_features,"modifier_name")
    return df

def values_counts_attribute_name(data:pd.DataFrame):
    list_features = []
    for d in data:

        attribute_list = []
        for ability in ["Q", "W", "E", "R"]:
            attribute_list.extend(d[ability]["attribute"])
    
        list_features.extend([x for x in attribute_list if x is not None])
    df = get_value_counts(list_features,"attribute_name")
    return df

def values_counts_champion(data:dict) -> pd.DataFrame:
    list_df = []
    for year, df in data.items():
        #print(df)
        df_champion = pd.DataFrame({"count":df.loc[df["champion"] != np.nan,"champion"].value_counts()}).reset_index()
        df_champion["year"] = year
        list_df.append(df_champion)
        print(df_champion)
    return pd.concat(list_df)
    ...
def get_value_counts(list_features:list,name_variable:str)-> pd.DataFrame:
    series_counts = pd.Series(list_features).value_counts()
    df = pd.DataFrame({name_variable: series_counts})
    df_counts = df[name_variable].reset_index()
    df_counts.columns = [name_variable, 'count']
    return df_counts
def split_data(data: pd.DataFrame, parameters: dict) -> tuple:
    """Splits data into features and targets training and test sets.

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters/data_science.yml.
    Returns:
        Split data.
    """
    X = data[parameters["features"]]
    y = data["price"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"]
    )
    return X_train, X_test, y_train, y_test


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    """Trains the linear regression model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for price.

    Returns:
        Trained model.
    """
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    return regressor


def evaluate_model(
    regressor: LinearRegression, X_test: pd.DataFrame, y_test: pd.Series
) -> dict[str, float]:
    """Calculates and logs the coefficient of determination.

    Args:
        regressor: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for price.
    """
    y_pred = regressor.predict(X_test)
    score = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    me = max_error(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("Model has a coefficient R^2 of %.3f on test data.", score)
    return {"r2_score": score, "mae": mae, "max_error": me}
