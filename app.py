"""
Streamlit app
"""
import joblib
import pandas as pd
import streamlit as st
from utils.clinical_trials_pubmed import ct_pm
from datetime import datetime

def main():

    # prepare variables for user input
    inn = ""
    orphan = ""
    therap_area = ""

    st.header("PharmaPredict")
    st.markdown("**Tell us something about your product**")
    inn = st.text_input("INN")
    orphan = st.radio("Orphan drug", ["Yes", "No"])
    therap_area = st.text_input("Therapeutic area")

    if ((inn != "") & (orphan != "") & (therap_area != "")):
        df_input = pd.DataFrame(data = [[inn, therap_area, orphan, datetime.now()]], columns=["INN", "Therapeutic area", "Orphan drug", "First published"])
        df_input

        df = ct_pm(df_input)
        df

if __name__ == "__main__":
    main()
