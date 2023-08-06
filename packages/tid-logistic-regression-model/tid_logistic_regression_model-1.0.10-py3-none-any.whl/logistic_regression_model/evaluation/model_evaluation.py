import os

import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score

from logistic_regression_model.parameters.project_parameters import font, save_ouptuts


def cross_validation(models, x, y, number_of_splits):
    """ Stratified cross validation """

    # Stratified cross validation for one model
    if len(models) == 2:
        results = []
        names = [models[0]]
        kfold = StratifiedKFold(n_splits=number_of_splits)
        cv_results = cross_val_score(models[1], x, y, cv=kfold, scoring="accuracy")
        results.append(cv_results)
        print(
            "%s: mean: %f std dev: (%f)" % (names, cv_results.mean(), cv_results.std())
        )

        plt.figure(figsize=(7, 7))
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.boxplot(results, labels=names)
        plt.ylabel("Accuracy", fontsize=12)
        plt.title(f"{number_of_splits}-fold cross-validation")
        plt.tight_layout()
        mpl.rc("font", **font)

        file_name = models[0] + "CV_Models.png"
        plt.savefig(os.path.join(save_ouptuts, file_name))
        plt.close()
    else:
        # Stratified cross validation for multiple models
        results = []
        names = []
        for name, model in models:
            kfold = StratifiedKFold(n_splits=number_of_splits)
            cv_results = cross_val_score(model, x, y, cv=kfold, scoring="accuracy")
            results.append(cv_results)
            names.append(name)
            print("%s: %f (%f)" % (name, cv_results.mean(), cv_results.std()))

        plt.figure(figsize=(7, 7))
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.boxplot(results, labels=names)
        plt.ylabel("Accuracy", fontsize=12)
        plt.title(f"{number_of_splits}-fold cross-validation")
        plt.tight_layout()
        mpl.rc("font", **font)
        file_name = name + "CV_Models.png"
        plt.savefig(os.path.join(save_ouptuts, file_name))
        plt.close()
    return cv_results


def confusion_matrix(best_model, x, y, model_name):
    """ Plot confusion matrix """
    fig, ax_ = plt.subplots(figsize=(8, 8))
    disp = plot_confusion_matrix(best_model, x, y, ax=ax_)
    plt.figure(figsize=(20, 20))
    disp.ax_.set_title("Confusion Matrix")
    file_name = model_name + "_Confusion_Matrix.png"
    fig.savefig(os.path.join(save_ouptuts, file_name))
    plt.close()
