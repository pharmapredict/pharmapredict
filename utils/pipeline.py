from paramas import NUMERICAL_COLUMNS
# pipeline first steps

def pipeline()
    preprocess = ColumnTransformer([('scale', RobustScaler(), NUMERICAL_COLUMNS)],remainder='passthrough')

    pipe = Pipeline(steps=[('pre', preprocess),
                          ('scaler', StandardScaler()),
                          ('forest', RandomForestClassifier(max_depth=2, random_state=0, class_weight='balanced')),
                          ])
    return pipe
