import pandas as pd
import json
from mca.ports.HeroInfo import HeroInfo
import time
import numpy as np
hero_info = HeroInfo()


def _is_true(x: pd.Series) -> pd.Series:
    return x == "t"


def _parse_percentage(x: pd.Series) -> pd.Series:
    x = x.str.replace("%", "")
    x = x.astype(float) / 100
    return x


def _parse_money(x: pd.Series) -> pd.Series:
    x = x.str.replace("$", "").str.replace(",", "")
    x = x.astype(float)
    return x
# src/meu_projeto/pipelines/data_processing/nodes.py
def preprocess_heroport_api(metadata_champion: pd.DataFrame):
    list_features = []
    j = 0
    for champion in metadata_champion:
        result = {"Q":{},"W":{},"E":{},"R":{},"passive":{}}
        result["champion"] = champion["champion"]
        if champion["champion"] == None:
            continue
        
        data = hero_info.get_hero_stats(champion["champion"])
        data_q = data["spells"]["Q"]
        data_w = data["spells"]["W"]
        data_e = data["spells"]["E"]
        data_r = data["spells"]["R"]
        data_passive = data["passive"]
        result["Q"]["effects"] = get_effects(data_q,"Q")
        result["W"]["effects"] = get_effects(data_w,"W")
        result["E"]["effects"] = get_effects(data_e,"E")
        result["R"]["effects"] = get_effects(data_r,"R")
        result["Q"]["damage"] = get_damage_types(data_q)
        result["W"]["damage"] = get_damage_types(data_w)
        result["E"]["damage"] = get_damage_types(data_e)
        result["R"]["damage"] = get_damage_types(data_r)
        result["Q"]["attribute"] = get_modifier(data_q,"Q")
        result["W"]["attribute"] = get_modifier(data_w,"W")
        result["E"]["attribute"] = get_modifier(data_e,"E")
        result["R"]["attribute"] = get_modifier(data_r,"R")
        
        result["passive"]["effects"] = get_effects(data_passive,"passive")
        result["passive"]["damage"] = get_damage_types(data_passive)
        list_features.append(result)        
    return list_features

def get_effects(data,spell):
    list_features = []
    if spell == "passive":
        for d_q in data:
            data_q_effects = d_q["effects"]
            for d_q_e in data_q_effects:
                data_q_effects_leveling = d_q_e["description"]
                list_features.append(data_q_effects_leveling)
    else:
        for d_q in data:
            data_q_effects = d_q["effects"]
            for d_q_e in data_q_effects:
                data_q_effects_leveling = d_q_e["leveling"]
                if len(data_q_effects_leveling) > 0:
                    for d_q_e_l in data_q_effects_leveling:
                        data_q_effects_leveling_modifiers = d_q_e_l["modifiers"]
                        if len(data_q_effects_leveling_modifiers) > 0:
                            for d_q_e_l_m in data_q_effects_leveling_modifiers:
                                if d_q_e_l_m["units"][0] != "":
                                    list_features.extend(set(d_q_e_l_m["units"]))
    return pd.unique(np.array(list_features)).tolist()
    ...

def get_damage_types(data):
    list_features = []
    for d_q in data:
        data_q_effects = d_q["damageType"]
        list_features.append(data_q_effects)
    return pd.unique(np.array(list_features)).tolist()

def get_modifier(data,spell):
    list_features = []
    if spell == "passive":
        return list_features
    else:
        for d_q in data:
            data_q_effects = d_q["effects"]
            for d_q_e in data_q_effects:
                data_q_effects_leveling = d_q_e["leveling"]
                if len(data_q_effects_leveling) > 0:
                    for d_q_e_l in data_q_effects_leveling:
                        list_features.append(d_q_e_l["attribute"])
    return pd.unique(np.array(list_features)).tolist()
    ...

def preprocess_match_history(data: pd.DataFrame) -> pd.DataFrame:
    
    ...
def preprocess_companies(companies: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses the data for companies.

    Args:
        companies: Raw data.
    Returns:
        Preprocessed data, with `company_rating` converted to a float and
        `iata_approved` converted to boolean.
    """
    companies["iata_approved"] = _is_true(companies["iata_approved"])
    companies["company_rating"] = _parse_percentage(companies["company_rating"])
    return companies


def preprocess_shuttles(shuttles: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses the data for shuttles.

    Args:
        shuttles: Raw data.
    Returns:
        Preprocessed data, with `price` converted to a float and `d_check_complete`,
        `moon_clearance_complete` converted to boolean.
    """
    shuttles["d_check_complete"] = _is_true(shuttles["d_check_complete"])
    shuttles["moon_clearance_complete"] = _is_true(shuttles["moon_clearance_complete"])
    shuttles["price"] = _parse_money(shuttles["price"])
    return shuttles


def create_model_input_table(
    shuttles: pd.DataFrame, companies: pd.DataFrame, reviews: pd.DataFrame
) -> pd.DataFrame:
    """Combines all data to create a model input table.

    Args:
        shuttles: Preprocessed data for shuttles.
        companies: Preprocessed data for companies.
        reviews: Raw data for reviews.
    Returns:
        Model input table.

    """
    rated_shuttles = shuttles.merge(reviews, left_on="id", right_on="shuttle_id")
    rated_shuttles = rated_shuttles.drop("id", axis=1)
    model_input_table = rated_shuttles.merge(
        companies, left_on="company_id", right_on="id"
    )
    model_input_table = model_input_table.dropna()
    return model_input_table
