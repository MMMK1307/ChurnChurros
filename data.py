from werkzeug.datastructures import FileStorage
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

    data["id"] = range(0, len(data))

    return ReadDataResponse.success(data, clean_message)


def round_time(seconds: int):
    return round((seconds / 60), 2)

def create_graphs(p_data: pd.DataFrame):

    # dist
    f = p_data.copy(deep=True)
    f["seconds_of_use"] = f["seconds_of_use"].apply(round_time)
    f = f.loc[f["churn"] == 1, ["churn", "seconds_of_use"]]
    f.plot(title="Distribuição de Churns por Tempo de Uso", kind="hist", column="seconds_of_use", ylabel="Tempo de Uso (m)", xlabel="Contador Clientes").get_figure().savefig('static/dist.png', dpi=300, bbox_inches='tight')

    # rel
    e = p_data.copy(deep=True)
    e = e.loc[(e["churn"] == 1) & (e["call_failure"] > 1)]
    e.plot(
        title="Relação de Falhas por Tempo de Uso de clientes churn",
        kind="scatter",
        x="seconds_of_use",
        y="call_failure",
        xlabel="Tempo de Uso (s)", ylabel="Quantidade de Falhas"
    ).get_figure().savefig("static/rel.png", dpi=300, bbox_inches="tight")

    # comparison
    d = p_data.copy(deep=True)
    d = d.loc[(d["complains"] == 1) | (d["churn"] == 1)].groupby(["complains", "churn"])["id"].count()
    d = d.rename({0: "N", 1: "S"})
    d.plot(title="Comparação | Reclamação e Churn", kind="bar", xlabel="Reclamações, Churn \n S = Sim | N = Não", ylabel="Quantidade Pessoas").get_figure().savefig('static/comp.png', dpi=300, bbox_inches='tight')

    return