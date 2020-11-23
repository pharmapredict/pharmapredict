# get data functions
# a generic method for installing the data
import pandas as pd
from datetime import datetime


PREDICTIVE_FEATURES=['org_industry',
 'n_trials',
 'phase_4',
 'org_other',
 'status_completed',
 'status_recruiting',
 'phase_3',
 'pm_results',
 'status_not_yet_recruiting',
 'phase_2']

def user_inputs():

    df_inputs= pd.DataFrame()

    df_inputs['INN']= input('Please input the Active Ingredients (INN) of your drug:')
    df_inputs['Therapeutic area']= input('Please input the Therapeutic area which you drug inted to treat:')
    df_inputs['date']= datetime.now()
    return df_inputs

def get_data(drop_8000=True):
    df = pd.read_csv('raw_data/wra_CT_PM_conclusions.csv')
    df.drop(columns='Unnamed: 0', inplace=True)
    if drop_8000:
        df = df[df['n_trials'] < 8000]
    df.conclusions.fillna('',inplace=True)
    df = df.reset_index(drop=True)
    #df['therapeutic_number'] = df['Therapeutic area'].apply(lambda x: x.count(',') + 1)
    return df

# possibly include the feature list here as well - see above

# get numericals...and feature engineering

def get_numericals(df):
    df['therapeutic_number'] = df['Therapeutic area'].apply(lambda x: x.count(',') + 1)
    df = df.select_dtypes(exclude='object')
    return df

# trial columns as a percent of n_trials

TRIAL_COLUMNS=['status_not_yet_recruiting', 'status_recruiting',
       'status_enrolling_by_invitation', 'status_active_not_recruiting',
       'status_suspended', 'status_terminated', 'status_completed',
       'status_withdrawn', 'status_unknown', 'org_fed', 'org_indiv',
       'org_industry', 'org_network', 'org_nih', 'org_other', 'org_other_gov',
       'phase_early_1', 'phase_not_applicable', 'phase_1', 'phase_2',
       'phase_3', 'phase_4']

def percentage_columns(x, trial_columns):
    for column in trial_columns:
        df[column]=((df[column])/df['n_trials']).replace([np.inf, -np.inf, np.nan], 0)
    return df
