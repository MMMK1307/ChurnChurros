import dataclasses

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


@dataclasses.dataclass
class ModelModel:
    model: DecisionTreeClassifier | RandomForestClassifier
    accuracy: float
    x_mat: pd.DataFrame

    def predict_single(self, complains: bool, call_failure: int, seconds_of_use: int):
        predata = pd.DataFrame({
            "complains": [1 if complains else 0],
            "call_failure": [call_failure],
            "seconds_of_use": [seconds_of_use],
        })
        prediction = self.model.predict(predata)
        return prediction[0]

    def model_name_str(self):
        return f"{str(self.model.__class__.__name__)}"

    def confusion_str(self):
        return f"{self.x_mat}"


class Context:
    data: pd.DataFrame | None = None
    models: list[ModelModel] = []

@dataclasses.dataclass
class ReadDataResponse:
    data: pd.DataFrame | None
    text: str

    @staticmethod
    def error(text):
        return ReadDataResponse(None, text)

    @staticmethod
    def success(data: pd.DataFrame, text: str = ""):
        return ReadDataResponse(data, text)