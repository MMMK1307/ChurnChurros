from flask import Flask, render_template, request, Response, jsonify

import c_train
import data
from models import Context

app = Flask("TrashScrapePy")
_context = Context()


def bad_request(error: str):
    json_data = jsonify(error=error)
    return Response(json_data.data , 400)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/graphs", methods=["GET"])
def graphs():
    if _context.data is not None:
        data.create_graphs(_context.data)
    return render_template("graphs.html")


@app.route("/submit-data", methods=["POST"])
def file_submit():
    file = request.files.get('data-file')

    if file is None:
        return bad_request("Nenhum arquivo selecionado")

    data_response = data.read_file(file)

    if data_response.data is None:
        return bad_request(data_response.text)

    import c_train
    _context.data = data_response.data
    _context.models = c_train.train_models(data_response.data)
    data_response.text += " | Modelos Treinados..."

    return jsonify({"text": data_response.text})


@app.route("/tests", methods=["GET"])
def tests():
    return render_template("tests.html", models=_context.models)


@app.route("/test-data", methods=["POST"])
def test_data():
    if _context.data is None or len(_context.models) <= 0:
        return bad_request("qhat? O sistema está faminto. Nenhum dado foi assimilado")

    try:
        complains = request.form.get("complains", "0") == '1'
        call_failure = int(request.form.get("fail_count", "0"))
        use_time = int(request.form.get("use_time", "0"))
        model_id = int(request.form.get("model_id", "0"))
    except ValueError:
        return bad_request("Valores Inválidos")

    if model_id < 0 or model_id >= len(_context.models):
        return bad_request("Modelo Inválido")

    prediction = _context.models[model_id].predict_single(complains, call_failure, use_time)

    return jsonify({"prediction": prediction, **request.form.to_dict()})


def main():
    app.run(
        debug=True,
    )


if __name__ == '__main__':
    main()
