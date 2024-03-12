from typing import List
import pandas as pd

def get_interaction_from_line(line: str) -> str:
    """
    Get pairwise interaction in format AtomNumber1AtomNumber2 from set of lines, it is to be used withing list comprehension
    """
    interaction =  line.split(':')[1].split('->')[0] + line.split(':')[1].split('->')[1].split('(')[0]
    return interaction

def get_list_indicator_from_path(path: str) -> str:
    """
    For ICOBILIST.lobster, ICOHPLIST.lobster, ICOOPLIST.lobster
    """
    END_LEN = len("LIST.lobster")
    filename = path.split('/')[-1]
    indicator = filename[:-END_LEN].lower()
    return indicator

def get_car_indicator_from_path(path: str) -> str:
    """
    For ICOBILIST.lobster, ICOHPLIST.lobster, ICOOPLIST.lobster
    """
    END_LEN = len("car.lobster")
    filename = path.split('/')[-1]
    indicator = filename[:-END_LEN].lower()
    return indicator

def multiply_by_minus_one(df: pd.DataFrame, excluding='E') -> pd.DataFrame:
    """
    For COHPCAR.lobster, all values except energy must be multiplied by -1
    """
    out_df = df.copy()
    to_muliply = out_df.columns.difference([excluding])
    out_df[to_muliply] = -1 * out_df[to_muliply]
    return out_df

def prep_list_df(df_arr: List[pd.DataFrame]) -> pd.DataFrame:
    """
    concat and pivot list df array
    """
    concat_df = pd.concat(df_arr, ignore_index=True)
    out_df = pd.pivot(concat_df, index='structure', columns='interaction', values='indicator')
    return out_df

def filter_df_by_energy(df, e_low, e_high):
    """
    Filter out dataframe rows outside energy bounds
    """
    out_df = df.copy()
    return out_df[(e_low < out_df['E']) & (out_df['E'] < e_high)] # THis is ugly