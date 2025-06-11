import pandas as pd
import numpy as np
from typing import Callable
from mca.utils.operations import calculate_mean


def graphic_scenarios_heatmap(data:dict) -> pd.DataFrame:
    list_df = []
    str_type = "pick"
    for year, df in data.items():
        df_champion = create_df(df,year,str_type)
        if df_champion.shape[0] > 0:
            list_df.append(df_champion)
    return pd.concat(list_df)

def calculate_kda(row):
    participation = row["kills"] + row["assists"] 
    if row["deaths"] == 0:
        return  round(participation,2)
    return round(participation/row["deaths"],2)

def create_df(df:pd.DataFrame,year:str,type_agg:str):
    df_only_champion = df.loc[df["champion"].notna()]
    if df_only_champion.empty:
        return pd.DataFrame()
    
    aggregation_functions: dict[str, Callable[[pd.DataFrame], pd.DataFrame]] = {
        "pick": get_pick_list,
        "damage": get_damage_list,
        "gold": get_gold_list,
        "minion":get_minion_list,
        "kda": get_kda_list
    }
    
    selected_function = aggregation_functions.get(type_agg)
    if selected_function:
        df_champion = selected_function(df_only_champion)
        df_champion["year"] = year
    else:
        df_champion = pd.DataFrame()
    return df_champion
def values_counts_champion(data:dict) -> pd.DataFrame:
    list_df = []
    str_type = "pick"
    for year, df in data.items():
        df_champion = create_df(df,year,str_type)
        if df_champion.shape[0] > 0:
            list_df.append(df_champion)
    return pd.concat(list_df)

def damage_counts_champion(data:dict)->pd.DataFrame:
    list_df = []
    str_type = "damage"
    for year, df in data.items():
        df_champion = create_df(df,year,str_type)
        if df_champion.shape[0] > 0:
            list_df.append(df_champion)
    
    
    
    #for year, df in data.items():
    #    df_only_champion = df.loc[df["champion"] != np.nan,:]
    #    df_champion = get_damage_list(df_only_champion)
    #    df_champion["year"] = year

    #    list_df.append(df_champion)
    return pd.concat(list_df)
def gold_counts_champion(data:dict)->pd.DataFrame:
    list_df = []
    str_type = "gold"
    for year, df in data.items():
        df_champion = create_df(df,year,str_type)
        if df_champion.shape[0] > 0:
            list_df.append(df_champion)
    return pd.concat(list_df)
def minion_counts_champion(data:dict)->pd.DataFrame:
    list_df = []
    str_type = "minion"
    for year, df in data.items():
        df_champion = create_df(df,year,str_type)
        if df_champion.shape[0] > 0:
            list_df.append(df_champion)
    return pd.concat(list_df)
def kda_counts_champion(data:dict)->pd.DataFrame:
    list_df = []
    str_type = "kda"
    for year, df in data.items():
        df_champion = create_df(df,year,str_type)
        if df_champion.shape[0] > 0:
            list_df.append(df_champion)
    return pd.concat(list_df)
    ...
def get_pick_list(df:pd.DataFrame)->pd.DataFrame:
    df_champion = df.groupby("champion").agg(wins=("result","sum"),
                                             win_ratio=("result",lambda x: calculate_mean(x)),
                                             pick=("champion","count")).reset_index()
    return df_champion

def get_damage_list(df: pd.DataFrame)-> pd.DataFrame:
    df_damage = df.groupby("champion").agg(
        damage_champion=("damagetochampions",lambda x: calculate_mean(x)),
        damage_champion_per_minute=("dpm",lambda x: calculate_mean(x))
    ).reset_index()
    return pd.DataFrame(df_damage)

def get_gold_list(df: pd.DataFrame)->pd.DataFrame:
    df_damage = df.groupby("champion").agg(
        total_gold=("totalgold",lambda x: calculate_mean(x)),
        earned_gold=("earnedgold",lambda x: calculate_mean(x)),
        earned_gpm=("earned gpm",lambda x: calculate_mean(x))
    ).reset_index()
    return pd.DataFrame(df_damage)

def get_minion_list(df: pd.DataFrame)->pd.DataFrame:
    df_damage = df.groupby("champion").agg(
        total_cs=("total cs",lambda x: calculate_mean(x)),
        minion_kills=("minionkills",lambda x: calculate_mean(x)),
        monster_kills=("monsterkills",lambda x: calculate_mean(x))
    ).reset_index()
    return pd.DataFrame(df_damage)

def get_kda_list(dfa: pd.DataFrame)->pd.DataFrame:
    df = dfa.copy() 
    df.loc[:,"kda"] = df.apply(lambda row: calculate_kda(row),axis=1)
    df_damage = df.groupby("champion").agg(
        games = ("champion","count"),
        kills = ("kills",lambda x: calculate_mean(x)),
        deaths= ("deaths",lambda x: calculate_mean(x)),
        assists = ("assists",lambda x: calculate_mean(x)), 
        kda= ("kda",lambda x: calculate_mean(x))
    ).reset_index()
    return pd.DataFrame(df_damage)
    ...

def versus_matchus(data: dict)->dict:
    result_final = {}
    for year, df in data.items():
        list_champion =  df["champion"].unique().tolist()
        list_df = []
        
        for champion in list_champion:
            if champion != np.nan:
                list_games = pd.unique(df.loc[df["champion"] == champion,"gameid"]).tolist()
                df_scenarios = df.loc[df["gameid"].isin(list_games),:]
                #print(df_scenarios)
                result_scenario = versus_champion_scenario(champion,df_scenarios,year)
                list_df.append(result_scenario)
            #if champion not in result_final.keys():
            #    result_final[champion] = {year:result_scenario}
            #else:
            #    result_final[champion].update({year:result_scenario})
        #print(list_champion)
        result_final[year] = pd.concat(list_df).reset_index(drop=True)

    return result_final

def versus_champion_scenario(champion:str,df_champion:pd.DataFrame,year:str)->list:
    roles = pd.unique(df_champion.loc[df_champion["champion"] == champion,"position"]).tolist()
    result = []
    for r in roles:
        game_id = df_champion.loc[(df_champion["position"] == r)&
                                  (df_champion["champion"] == champion)
                                  ,"gameid"]
        df_role = df_champion.loc[(df_champion["gameid"].isin(game_id))&
                                  (df_champion["position"] == r)&
                                  (df_champion["champion"] != champion)]
        data_result = df_role.groupby("champion").agg(
                            win_ratio=("result",lambda x: round(1 - calculate_mean(x),2)),
                            loss_ratio=("result",lambda x: calculate_mean(x)),
                            loss=("result","sum"),
                            pick=("champion","count")
                            )
        data_result.index.rename("champion_vs",inplace=True)
        data_result["wins"] = data_result["pick"] - data_result["loss"]
        data_result["role"] = r
        data_result["champion_main"] = champion
        #if champion == "Trundle" and year == "2014":
        #    print(data_result)
        
        #result.append({r:data_result.to_dict(orient="index")})
        result.append(data_result.reset_index())
    if len(result) == 0:
        df = pd.DataFrame()
    else:
        df = pd.concat(result)
    return df