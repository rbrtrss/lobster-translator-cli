import pandas as pd
from io import StringIO
from .helpers import get_interaction_from_line
from .helpers import get_indicator_from_path
from .helpers import multiply_by_minus_one

def carfile_to_df(input_path: str):
    """
    To read COHPCAR.lobster, COBICAR.lobster or COOPCAR.lobster and collect in pd.Dataframe
    """
    # Read the file content
    with open(input_path, 'r') as file:
        lines = file.readlines()

    filename = input_path.split('/')[-1]
    structure = input_path.split('/')[-2]

    interactions = [get_interaction_from_line(line) for line in lines if line.startswith("No.")]
    integrated_interactions = ['i' + interaction for interaction in interactions]
    alternating = [element for pair in zip(interactions,integrated_interactions) for element in pair] # This looks very arcane

    # Data starts after interactions, join the remaining lines
    data = ''.join(lines[(3 + len(interactions)):])

    # Read the data into a DataFrame
    df = pd.read_csv(StringIO(data), delim_whitespace=True, header=None)

    # Rename columns
    df.columns = ['E', 'total', 'itotal'] + alternating

    if filename == 'COHPCAR.lobster':
        df = multiply_by_minus_one(df)

    # df['structure'] = structure

    return structure, df

def listfile_to_df(input_path: str):
    """
    To read ICOBILIST.lobster, ICOHPLIST.lobster or ICOOPLIST.lobster and collect in pd.DataFrame
    """
    structure = input_path.split('/')[-2]
    df = pd.read_csv(input_path, sep=r'\s+', engine='python', skiprows=1, header=None)
    indicator = get_indicator_from_path(input_path)
    df['structure'] = structure
    df['interaction'] = df[1] + df[2]
    df[indicator] = df[7]
    df['distance'] = df[3]
    return indicator, df[['structure','interaction',indicator, 'distance']]

