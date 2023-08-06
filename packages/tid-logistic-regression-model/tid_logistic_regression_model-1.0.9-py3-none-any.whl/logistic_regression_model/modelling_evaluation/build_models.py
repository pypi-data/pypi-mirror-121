from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC


def logistic_reg_model(X_train, y_train):
    """ Build logistic regression model """
    logistic_regression_model = LogisticRegression(
        multi_class="multinomial", max_iter=100, class_weight="balanced"
    ).fit(X_train, y_train)
    return logistic_regression_model


def svm_model():
    SVM_model = LinearSVC()
    return SVM_model


def random_forest_model(number_of_estimators):
    RF_model = RandomForestClassifier(n_estimators=number_of_estimators, random_state=0)
    return RF_model


def naive_bayes_model():
    NB = MultinomialNB()
    return NB
