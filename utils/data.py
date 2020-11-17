# get data functions
# a generic method for installing the data
import pandas as pd


def get_data(drop_8000=True):
    df = pd.read_csv('../raw_data/enriched_CT_PM.csv')
    df.drop(columns='Unnamed: 0', inplace=True)
    if drop_8000:
        df = df[df['n_trials'] < 8000]
    return df

# possibly include the feature list here as well
