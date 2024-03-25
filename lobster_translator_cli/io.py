import pandas as pd
from io import StringIO
from .helpers import get_interaction_from_line
from .helpers import get_list_indicator_from_path
from .helpers import get_car_indicator_from_path
from .helpers import multiply_by_minus_one
from .helpers import filter_df_by_energy

def carfile_to_df(input_path: str, energy_range):
    """
    To read COHPCAR.lobster, COBICAR.lobster or COOPCAR.lobster and collect in pd.Dataframe
    """
    # Read the file content
    with open(input_path, 'r') as file:
        lines = file.readlines()

    indicator = get_car_indicator_from_path(input_path)
    structure = input_path.split('/')[-2]

    interactions = [get_interaction_from_line(line) for line in lines if line.startswith("No.")]
    integrated_interactions = ['i' + interaction for interaction in interactions]
    alternating = [element for pair in zip(interactions,integrated_interactions) for element in pair] # This looks very arcane

    # Data starts after interactions, join the remaining lines
    data = ''.join(lines[(3 + len(interactions)):])

    # Read the data into a DataFrame
    df = pd.read_csv(StringIO(data), sep='\s+', header=None)

    # Rename columns
    df.columns = ['E', 'total', 'itotal'] + alternating

    if indicator == 'cohp':
        df = multiply_by_minus_one(df)

    # df['structure'] = structure
    if energy_range is not None:
        e_down, e_up = energy_range    
        df = filter_df_by_energy(df,e_down,e_up)

    return indicator, structure, df

def listfile_to_df(input_path: str):
    """
    To read ICOBILIST.lobster, ICOHPLIST.lobster or ICOOPLIST.lobster and collect in pd.DataFrame
    """
    structure = input_path.split('/')[-2]
    df = pd.read_csv(input_path, sep=r'\s+', engine='python', skiprows=1, header=None)
    indicator = get_list_indicator_from_path(input_path)
    df['structure'] = structure
    df['interaction'] = df[1] + df[2]
    if indicator == 'icohp':
        df[7] = -1 * df[7]
    df['indicator'] = df[7]
    # df['distance'] = df[3] see bellow listfile_distance_df function
    out_df = df[['structure', 'interaction', 'indicator']]
    # out_df.set_index('interaction')
    return indicator, out_df

def listfile_distance_df(input_path: str):
    """
    To create a distance indicator from ICOXXLIST.lobster files (distance is in a different position hence the need for an special function)
    """
    structure = input_path.split('/')[-2]
    df = pd.read_csv(input_path, sep=r'\s+', engine='python', skiprows=1, header=None)
    indicator = 'distance'
    df['structure'] = structure
    df['interaction'] = df[1] + df[2]
    df['indicator'] = df[3]
    out_df = df[['structure', 'interaction', 'indicator']]
    return indicator, out_df



# def listfile_to_df(input_path: str):
#     """
#     To read ICOBILIST.lobster, ICOHPLIST.lobster or ICOOPLIST.lobster and collect in pd.DataFrame
#     """
#     structure = input_path.split('/')[-2]
#     df = pd.read_csv(input_path, sep=r'\s+', engine='python', skiprows=1, header=None)
#     indicator = get_indicator_from_path(input_path)
#     df['structure'] = structure
#     df['interaction'] = df[1] + df[2]
#     df[indicator] = df[7]
#     df['distance'] = df[3]
#     return indicator, df[['structure','interaction',indicator, 'distance']]