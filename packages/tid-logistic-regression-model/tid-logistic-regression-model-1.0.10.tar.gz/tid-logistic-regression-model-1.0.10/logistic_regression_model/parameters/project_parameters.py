# import os

from pathlib import Path

import logistic_regression_model

# Define global font for EDA
font = {"family": "calibri", "weight": "normal", "size": 18}

url_list_bbc = [
    "https://www.bbc.co.uk/sport/football",
    "https://www.bbc.co.uk/sport/formula1",
    "https://www.bbc.co.uk/sport/cricket",
    "https://www.bbc.co.uk/sport/tennis",
]

url_list_sky_sports = [
    "https://www.skysports.com/football",
    "https://www.skysports.com/f1",
    "https://www.skysports.com/cricket",
    "https://www.skysports.com/tennis",
]

# Save outputs
project_path = Path(logistic_regression_model.__file__).resolve().parent

# project_path = r"C:\Users\Aiden\Documents\Data_Science_Stuff\sf_Data_Science_Stuff\Projects\06_ML_Deployment\01_Build_Package\logistic_regression_model"
input_folder = "input_data"
output_folder = "outputs"
models_folder = "saved_models"
# save_ouptuts = os.path.join(project_path, output_folder)
# save_input = os.path.join(project_path, input_folder)
# save_models = os.path.join(project_path, models_folder)

save_ouptuts = project_path / output_folder
save_input = project_path / input_folder
save_models = project_path / models_folder

# Dataset to use
training_data = "Sports_News_09_09_2021.csv"
# training_dataset_path = os.path.join(save_input, training_data)
training_dataset_path = save_input / training_data

testing_data = "Sports_News_03_06_2021.csv"
# testing_dataset_path = os.path.join(save_input, testing_data)
testing_dataset_path = save_input / testing_data

# Trained Model and Vocabs
trained_model_name = "final_model.joblib"
vec_file = "count_vector.pkl"
tfidf_file = "tfidf.pkl"

# file_path_model = os.path.join(save_models, trained_model_name)
# file_path_vec = os.path.join(save_models, vec_file)
# file_path_tfidf = os.path.join(save_models, tfidf_file)

file_path_model = save_models / trained_model_name
file_path_vec = save_models / vec_file
file_path_tfidf = save_models / tfidf_file
