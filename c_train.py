
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

from models import ModelModel

RAND_STATE = 65


def _create_model(d_data: pd.DataFrame, model: DecisionTreeClassifier | RandomForestClassifier):
    x_data = d_data[["complains", "call_failure", "seconds_of_use"]]
    y_data = d_data["churn"]

    x_train, x_test, y_train, y_test = train_test_split(
        x_data, y_data, test_size=0.20, random_state=RAND_STATE
    )

    model.fit(x_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(x_test))
    c_mat = confusion_matrix(y_test, model.predict(x_test))

    return ModelModel(model, accuracy, c_mat)


def train_models(d_data: pd.DataFrame):
    return [get_model_1(d_data), get_model_2(d_data)]


def get_model_1(d_data: pd.DataFrame) -> ModelModel:
    return _create_model(d_data, DecisionTreeClassifier(random_state=RAND_STATE))


def get_model_2(d_data: pd.DataFrame) -> ModelModel:
    return _create_model(d_data, RandomForestClassifier(random_state=RAND_STATE))