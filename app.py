"""
Streamlit app
"""
import pandas as pd
import streamlit as st
from utils.clinical_trials_pubmed import ct_pm
from utils.data import input_to_df
from utils.data import get_numericals
from joblib import load
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

from datetime import datetime

def main():

    scaler = load('models/scaler.joblib')
    vectorizer = load('models/vectorizer.joblib')
    model = load('models/random_forest_clf.joblib')

    # prepare variables for user input
    inn = ""
    orphan = ""
    therap_area = ""

    st.header("PharmaPredict")
    st.markdown("**Tell us something about your product**")
    inn = st.text_input("INN")
    orphan = st.radio("Orphan drug", ["yes", "no"])
    therap_area = st.text_input("Therapeutic area")

    # checking if user input is valid
    if ((inn != "") & (orphan != "") & (therap_area != "")):
        df_input = pd.DataFrame(data = [[inn, therap_area, orphan, datetime.now()]], columns=["INN", "Therapeutic area", "Orphan medicine", "First published"])
        df_input["Orphan medicine"] = df_input["Orphan medicine"].map({"no" : 0, "yes": 0})
        st.write(df_input)

        df = ct_pm(df_input)
        st.write(df)

        # create text features using fitted TfIdf vectorizer
        vectorized = input_to_df(df, vectorizer)
        st.write(df)

        # scale
        numericals = get_numericals(df)
        columns_names = numericals.columns.to_list()
        columns_names
        scaled_array = scaler.transform(numericals[columns_names])
        scaled_numericals = pd.DataFrame(scaled_array, columns=columns_names)
        X = scaled_numericals.join(vectorized)
        X

        # predict
        y_pred = model.predict(X)
        st.write(y_pred)


if __name__ == "__main__":
    main()
