import pickle
import typing as t

import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from logistic_regression_model.data_prep.validation import validate_inputs
from logistic_regression_model.parameters.project_parameters import (
    file_path_model,
    file_path_tfidf,
    file_path_vec,
)

# Load trained model and vocabs to make predictions
trained_model = joblib.load(filename=file_path_model)
loaded_vec = CountVectorizer(vocabulary=pickle.load(open(file_path_vec, "rb")))
loaded_tfidf = pickle.load(open(file_path_tfidf, "rb"))


def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """ Makes a prediction for dataframe of headlines"""

    # Make sure data is dataframe
    data = pd.DataFrame(input_data, columns={"Headline"})

    # Validate feature
    validated_data, errors = validate_inputs(input_data=data)

    # Placeholder for predictions
    results = {"predictions": None, "errors": errors}

    if not errors:
        validated_data_headlines = validated_data["Headline"].values.tolist()
        X_new_counts = loaded_vec.transform(validated_data_headlines)
        X_new_tfidf = loaded_tfidf.transform(X_new_counts)
        predictions = list(trained_model.predict(X_new_tfidf))

        results = {"predictions": predictions, "errors": errors}

    return results
