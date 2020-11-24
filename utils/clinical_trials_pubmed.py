import pandas as pd
import time
from pharmatools.clinical_trials import get_trial_data
from pharmatools.pubmed import get_pubmed_ids, get_titles_abstracts_batch
from nltk.tokenize import sent_tokenize

"""
functions to enrich a pandas dataframe (INN, therapeutic areas, date) with
clinicaltrials.gov and PubMed data
"""


def ct_pm(df):
    """
    combining below functions to enrich dataset
    """
    df = trial_data(df)
    df = pubmed_conclusions(df)
    return df


def trial_data(df):
    """
    enriching dataframe with data on clinical trials
    from clinicaltrials.gov API
    """
    # convert to datetime
    df["First published"] = pd.to_datetime(df["First published"])

    # prepare dataframe
    df["n_trials"] = 0
    df["status_not_yet_recruiting"] = 0
    df["status_recruiting"] = 0
    df["status_enrolling_by_invitation"] = 0
    df["status_active_not_recruiting"] = 0
    df["status_suspended"] = 0
    df["status_terminated"] = 0
    df["status_completed"] = 0
    df["status_withdrawn"] = 0
    df["status_unknown"] = 0

    df["org_fed"] = 0
    df["org_indiv"] = 0
    df["org_industry"] = 0
    df["org_network"] = 0
    df["org_nih"] = 0
    df["org_other"] = 0
    df["org_other_gov"] = 0

    df["phase_early_1"] = 0
    df["phase_not_applicable"] = 0
    df["phase_1"] = 0
    df["phase_2"] = 0
    df["phase_3"] = 0
    df["phase_4"] = 0

    # pull data from API into dataframe
    for index, row in df.iterrows():

        print(f'fetching trial data for {index}, {row["INN"]}')

        # call ClinicalTrials API
        attempts = 0
        while attempts < 3:
            try:
                data = get_trial_data(
                    row["INN"], row["Therapeutic area"], row["First published"]
                )

                # update dataframe
                df["n_trials"][index] = data["n_trials"]

                df["status_not_yet_recruiting"][index] = data["status"][
                    "Not yet recruiting"
                ]
                df["status_recruiting"][index] = data["status"]["Recruiting"]
                df["status_enrolling_by_invitation"][index] = data["status"][
                    "Enrolling by invitation"
                ]
                df["status_active_not_recruiting"][index] = data["status"][
                    "Active, not recruiting"
                ]
                df["status_suspended"][index] = data["status"]["Suspended"]
                df["status_terminated"][index] = data["status"]["Terminated"]
                df["status_completed"][index] = data["status"]["Completed"]
                df["status_withdrawn"][index] = data["status"]["Withdrawn"]
                df["status_unknown"][index] = data["status"]["Unknown status"]

                df["org_fed"][index] = data["organizers"]["FED"]
                df["org_indiv"][index] = data["organizers"]["INDIV"]
                df["org_industry"][index] = data["organizers"]["INDUSTRY"]
                df["org_network"][index] = data["organizers"]["NETWORK"]
                df["org_nih"][index] = data["organizers"]["NIH"]
                df["org_other"][index] = data["organizers"]["OTHER"]
                df["org_other_gov"][index] = data["organizers"]["OTHER_GOV"]

                df["phase_early_1"][index] = data["phases"]["Early Phase 1"]
                df["phase_not_applicable"][index] = data["phases"]["Not Applicable"]
                df["phase_1"][index] = data["phases"]["Phase 1"]
                df["phase_2"][index] = data["phases"]["Phase 2"]
                df["phase_3"][index] = data["phases"]["Phase 3"]
                df["phase_4"][index] = data["phases"]["Phase 4"]
                break
            except:
                print("fetching trial data not successful")
                time.sleep(0.5)
                attempts += 1

    return df


def pubmed_abstracts(df):
    """
    get abstracts for each row in a dataframe from PubMed
    """

    df_abstracts = pd.DataFrame(columns=["id", "abstract"])
    df["pm_results"] = 0

    for index, row in df.iterrows():
        print(f"index: {index}, INN: {row['INN']}")
        ids = get_pubmed_ids(
            row["INN"], row["Therapeutic area"], row["First published"]
        )
        n_ids = len(ids)
        print(f"results: {n_ids}")
        df["pm_results"][index] = n_ids

        # fetch abstracts of first 200 results
        titles, abstracts = get_titles_abstracts_batch(ids[:200])
        print(f"# of abstracts: {len(abstracts)}")
        for abstract in abstracts:
            df_abstracts = df_abstracts.append(
                pd.DataFrame.from_dict({"id": [index], "abstract": [abstract]}),
                ignore_index=True,
            )
        print("")

        return df_abstracts


def n_last_senteces(text, n):
    """
    returns the last 2 sentences of a text
    """
    return " ".join(sent_tokenize(text)[-n:])


def pubmed_conclusions(df):
    """
    enriching a dataframe by conclusions (last 2 sentences of each abstract)
    from PubMed
    """

    df_abstracts = pubmed_abstracts(df)

    df["conclusions"] = ""
    for index, row in df.iterrows():
        print(index)
        conclusions = ""
        for _, row_abstr in df_abstracts.loc[df_abstracts["id"] == index].iterrows():
            conclusion = n_last_senteces(row_abstr["abstract"], 2)
            conclusions += " " + conclusion
        df["conclusions"][index] = conclusions

    return df
