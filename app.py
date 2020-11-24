"""
Streamlit app
"""
import pandas as pd
import streamlit as st
from utils.clinical_trials_pubmed import ct_pm, trial_data, pubmed_conclusions
from utils.data import input_to_df
from utils.data import get_numericals
from joblib import load
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

from datetime import datetime


def main():

    # load fitted scaler, vectorizer and model
    scaler = load("models/scaler.joblib")
    vectorizer = load("models/vectorizer.joblib")
    model = load("models/random_forest_clf.joblib")

    # prepare variables for user input
    inn = ""
    orphan = ""
    therap_area = ""

    st.header("PharmaPredict")
    st.markdown("**Tell us something about your product**")

    # user input
    inn = st.text_input("INN (international nonproprietary name)")
    therap_area = st.text_input("Therapeutic area (if more than one, separate by comma")
    orphan = st.radio("Orphan drug", ["yes", "no"])

    st.markdown("**Gathering additional data**")
    trials_progress = st.markdown("🕒 Trial data from ClinicalTrials.gov")
    pubmed_progress = st.markdown("🕒 Abstracts from PubMed")

    st.markdown("**Prediction**")
    prediction_placeholder = st.markdown("🕒 Waiting for you input")

    # checking if user input is valid
    if (inn != "") & (orphan != "") & (therap_area != ""):

        prediction_placeholder.markdown("🕒 Waiting for additional data")

        # turn user input into dataframe
        df_input = pd.DataFrame(
            data=[[inn, therap_area, orphan, datetime.now()]],
            columns=["INN", "Therapeutic area", "Orphan medicine", "First published"],
        )

        # encode Orphan medicine column
        df_input["Orphan medicine"] = df_input["Orphan medicine"].map(
            {"no": 0, "yes": 0}
        )

        # get clinical trials and pubmed columns
        #df_ct_pm = ct_pm(df_input)
        trials_progress.markdown("👉 Trial data from ClinicalTrials.gov")
        df_ct = trial_data(df_input)
        trials_progress.markdown("✔ Trial data from ClinicalTrials.gov")
        pubmed_progress.markdown("👉 Abstracts from PubMed")
        df_ct_pm = pubmed_conclusions(df_ct)
        pubmed_progress.markdown("✔ Abstracts from PubMed")

        # create text features using fitted TfIdf vectorizer
        vectorized = input_to_df(df_ct_pm, vectorizer)

        # scale
        numericals = get_numericals(df_ct_pm)
        columns_names = numericals.columns.to_list()
        scaled_array = scaler.transform(numericals[columns_names])
        scaled_numericals = pd.DataFrame(scaled_array, columns=columns_names)
        X = scaled_numericals.join(vectorized)

        # predict
        prediction_placeholder.empty()
        y_pred = model.predict_proba(X)
        st.write(
            "The probabilty of market authorisation is: {:.0%}".format(y_pred[0][0])
        )
        


if __name__ == "__main__":
    main()
