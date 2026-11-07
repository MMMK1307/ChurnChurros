from werkzeug.datastructures import FileStorage
import pandas as pd

from models import ReadDataResponse

required_fields = {"complains", "call_failure", "seconds_of_use", "churn"}


def read_file(file: FileStorage) -> ReadDataResponse:
    try:
        raw_data : pd.DataFrame = pd.read_csv(file.stream)
    except:
        return ReadDataResponse.error("Arquivo Inválido!!!")
    data = pd.DataFrame()

    col_count = 0

    for col_name, col_data in raw_data.items():
        col_name_l = str(col_name).replace("  ", " ").replace(" ", "_").lower()
        if col_name_l in required_fields:
            data[col_name_l] = col_data
            col_count += 1

    if len(required_fields) != col_count:
        return ReadDataResponse.error("Campos Necessário não foram informados")

    clean_message = f"Dados Assimilados. Total items: {len(data)}"
    data = data.dropna()
    clean_message += f" | Após limpeza: {len(data)}"
    clean_message += f" | Campos: {data.columns}"

    return ReadDataResponse.success(data, clean_message)