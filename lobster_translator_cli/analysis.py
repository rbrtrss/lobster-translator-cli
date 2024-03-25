import pandas as pd
from .io import carfile_to_df


def full_car(lobster_dict,energy_range):
    car_arr = lobster_dict["car"]
    all_car_list = [ car_df_with_indicator_and_structure(car, energy_range) for car in car_arr ]
    all_car_df = pd.concat(all_car_list, ignore_index=True)
    return all_car_df


def car_df_with_indicator_and_structure(car_path, energy_range):
    indicator, structure, df = carfile_to_df(car_path, energy_range)
    df["indicator"] = indicator
    df["structure"] = structure
    return df