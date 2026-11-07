import dataclasses

import pandas as pd


class Context:
    data: pd.DataFrame


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