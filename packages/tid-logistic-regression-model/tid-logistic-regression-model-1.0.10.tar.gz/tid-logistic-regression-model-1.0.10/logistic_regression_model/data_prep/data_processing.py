# import os
# from pathlib import Path
import pickle
from datetime import date

import pandas as pd
from parameters.project_parameters import save_input, save_models
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split


def data_processing(dataset_combined):
    """Performs data processing of both datasets
    If flag is set True, CSV of dataset is saved
    """
    # perform tfidf transformation
    X = dataset_combined.iloc[:, 0]  # extract column with headlines
    y = dataset_combined.iloc[:, -1]  # extract column with labels
    X_vec = tfidf_transform(X)

    return X_vec, y


def rename_class(dataset_combined):
    """ Renames class """
    dataset_combined = check_classes(dataset_combined)
    return dataset_combined


def combine_dataset(dataset_1, dataset_2, flag):
    """ Combines two datasets """
    dataset_combined = pd.concat([dataset_1, dataset_2])

    # save_to_csv
    if flag is True:
        save_to_csv(dataset_combined)

    return dataset_combined


def save_to_csv(dataset):
    """ Saves dataset as csv with today's date """

    today_date = date.today().strftime("%d_%m_%Y")
    file_name = "Sports_News_" + today_date + ".csv"
    # dataset.to_csv(os.path.join(save_input, file_name), index=False)
    dataset.to_csv(save_input / file_name, index=False)


def check_classes(dataset):
    """ Checks classes of news """

    # Change formula1 to f1
    dataset["Sport"] = dataset["Sport"].replace(["formula1"], ["f1"])

    return dataset


def count_vectorise(x):
    """ Perform count vectorisation """
    vectorizer = CountVectorizer(stop_words="english")
    X_vec = vectorizer.fit_transform(x)
    X_vec.todense()  # convert sparse matrix into dense matrix

    # SAVE WORD VECTOR
    # file_path = os.path.join(save_models, "count_vector.pkl")
    file_path = save_models / "count_vector.pkl"
    pickle.dump(vectorizer.vocabulary_, open(file_path, "wb"))

    return X_vec


def tfidf_transform(x):
    """ TFIDF transformation """
    tfidf = TfidfTransformer()
    x_vec = count_vectorise(x)
    X_tfidf = tfidf.fit_transform(x_vec)
    X_tfidf = X_tfidf.todense()

    # SAVE TF-IDF
    # file_path = os.path.join(save_models, "tfidf.pkl")
    file_path = save_models / "tfidf.pkl"
    pickle.dump(tfidf, open(file_path, "wb"))

    return X_tfidf


def split_dataset(x_tfidf, y, test_size_split):
    """ Split dataset into training and testing """
    X_train, X_test, y_train, y_test = train_test_split(
        x_tfidf, y, test_size=test_size_split, random_state=0
    )

    return X_train, X_test, y_train, y_test


# def make_prediction(model, headline):

# headline = [headline]

# LOAD MODEL
# loaded_vec = CountVectorizer(vocabulary=pickle.load(open("count_vector.pkl", "rb")))
# loaded_tfidf = pickle.load(open("tfidf.pkl", "rb"))
# loaded_model = pickle.load(open("nb_model.pkl","rb"))

# X_new_counts = loaded_vec.transform(headline)
# X_new_tfidf = loaded_tfidf.transform(X_new_counts)
# predicted = model.predict(X_new_tfidf)

# return "".join(predicted)
