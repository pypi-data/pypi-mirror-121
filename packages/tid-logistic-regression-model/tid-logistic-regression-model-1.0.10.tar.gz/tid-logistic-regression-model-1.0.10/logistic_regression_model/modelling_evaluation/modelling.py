# import os

import pandas as pd
from data_prep.data_processing import data_processing, rename_class, split_dataset
from evaluation.model_evaluation import confusion_matrix, cross_validation
from joblib import dump
from modelling_evaluation.build_models import logistic_reg_model
from parameters.project_parameters import save_models, training_dataset_path


def model_eval():

    # scrape data
    print("Loading data")
    dataset_combined = pd.read_csv(training_dataset_path)

    # process_datasets
    print("Processing data for machine learning...")
    dataset_combined = rename_class(dataset_combined)
    X_vec, y = data_processing(dataset_combined)

    # Split into training and testing (0.3 for testing)
    X_train, X_test, y_train, y_test = split_dataset(X_vec, y, 0.3)
    print("Data processing complete")

    # Build machine learning models
    print("Building machine learning model...")
    log_reg = logistic_reg_model(X_train, y_train)

    # cross validation
    print("Performing stratified cross-validation...")
    models = ("Logistic Reg (baseline)", log_reg)
    cross_validation(models, X_train, y_train, 10)

    # confusion matrix
    print("Saving confusion matrix...")
    confusion_matrix(log_reg, X_train, y_train, "logistic_regression")

    # Save model to saved_models folder
    print("Saving model")
    pkl_filename = "final_model.joblib"
    with open(save_models / pkl_filename, "wb") as file:
        dump(log_reg, file)

    # with open(os.path.join(save_models, pkl_filename), "wb") as file:
    #   dump(log_reg, file)
