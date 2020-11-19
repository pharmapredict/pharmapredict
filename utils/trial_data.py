from pharmatools import get_trial_data

def trial_data(df):
    # convert to datetime
    df['First published'] = pd.to_datetime(df['First published'])

    # prepare dataframe
    df['n_trials'] = 0
    df['status_not_yet_recruiting'] = 0
    df['status_recruiting'] = 0
    df['status_enrolling_by_invitation'] = 0
    df['status_active_not_recruiting'] = 0
    df['status_suspended'] = 0
    df['status_terminated'] = 0
    df['status_completed'] = 0
    df['status_withdrawn'] = 0
    df['status_unknown'] = 0

    df['org_fed'] = 0
    df['org_indiv'] = 0
    df['org_industry'] = 0
    df['org_network'] = 0
    df['org_nih'] = 0
    df['org_other'] = 0
    df['org_other_gov'] = 0

    df['phase_early_1'] = 0
    df['phase_not_applicable'] = 0
    df['phase_1'] = 0
    df['phase_2'] = 0
    df['phase_3'] = 0
    df['phase_4'] = 0

    # pull data from API into dataframe
for index, row in df.iterrows():
    
    print(f'fetching trial data for {index}, {row["Medicine name"]}')

    # call ClinicalTrials API
    data = get_trial_data(row['INN'], row['Therapeutic area'], row['First published'])
    
    # update dataframe
    df['n_trials'][index] = data['n_trials']
    
    df['status_not_yet_recruiting'][index] = data['status']['Not yet recruiting']
    df['status_recruiting'][index] = data['status']['Recruiting']
    df['status_enrolling_by_invitation'][index] = data['status']['Enrolling by invitation']
    df['status_active_not_recruiting'][index] = data['status']['Active, not recruiting']
    df['status_suspended'][index] = data['status']['Suspended']
    df['status_terminated'][index] = data['status']['Terminated']
    df['status_completed'][index] = data['status']['Completed']
    df['status_withdrawn'][index] = data['status']['Withdrawn']
    df['status_unknown'][index] = data['status']['Unknown status']
    
    df['org_fed'][index] = data['organizers']['FED']
    df['org_indiv'][index] = data['organizers']['INDIV']
    df['org_industry'][index] = data['organizers']['INDUSTRY']
    df['org_network'][index] = data['organizers']['NETWORK']
    df['org_nih'][index] = data['organizers']['NIH']
    df['org_other'][index] = data['organizers']['OTHER']
    df['org_other_gov'][index] = data['organizers']['OTHER_GOV']
    
    df['phase_early_1'][index] = data['phases']['Early Phase 1']
    df['phase_not_applicable'][index] = data['phases']['Not Applicable']
    df['phase_1'][index] = data['phases']['Phase 1']
    df['phase_2'][index] = data['phases']['Phase 2']
    df['phase_3'][index] = data['phases']['Phase 3']
    df['phase_4'][index] = data['phases']['Phase 4']

    return df