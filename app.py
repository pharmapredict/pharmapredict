"""
Streamlit app
"""
import pandas as pd
import streamlit as st
from utils.clinical_trials_pubmed import ct_pm
from utils.data import input_to_df
from joblib import load
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

from datetime import datetime

def main():

    #raw_data = pd.read_csv('raw_data/wra_CT_PM_conclusions.csv')
    #dumped_fitted_scaler = 'models/scaler.joblib'
    vectorizer = load('models/vectorizer.joblib')
    #dumped_model = 'models/random_forest_clf.joblib'

    # prepare variables for user input
    inn = ""
    orphan = ""
    therap_area = ""

    st.header("PharmaPredict")
    st.markdown("**Tell us something about your product**")
    inn = st.text_input("INN")
    orphan = st.radio("Orphan drug", [1, 0])
    therap_area = st.text_input("Therapeutic area")

    if ((inn != "") & (orphan != "") & (therap_area != "")):
        df_input = pd.DataFrame(data = [[inn, therap_area, orphan, datetime.now()]], columns=["INN", "Therapeutic area", "Orphan drug", "First published"])
        df_input

        df = ct_pm(df_input)
        df

        df = input_to_df(df, vectorizer)
        df


if __name__ == "__main__":
    main()
