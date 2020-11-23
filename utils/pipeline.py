import pandas as pd
import numpy as np

from utils.params import NUMERICAL_COLUMNS
from utils.data import get_select_data

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
import pickle
from sklearn.ensemble import RandomForestClassifier

# pipeline first steps

def pipeline(X_train,y_train):
    preprocess = ColumnTransformer([('scale', RobustScaler(), NUMERICAL_COLUMNS),
                                    ('vectorize',
                                        TfidfVectorizer(max_df = 0.8, min_df=0.5, max_features = 50, ngram_range=(1, 1)),
                                        'conclusions')
                                    ],remainder='passthrough')

    pipe = Pipeline(steps=[('pre', preprocess),
                          ('scaler', StandardScaler()),
                          ('forest', RandomForestClassifier(max_depth=3, random_state=23, class_weight='balanced')),
                          ])

    final_pipe = pipe.fit(X_train, y_train)
    with open("../models/pipeline.pkl", "wb") as file:
        pickle.dump(final_pipe, file)

df = get_select_data()
X = df.drop(columns='Authorisation status')
y = df['Authorisation status']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
pipeline(X_train,y_train)
