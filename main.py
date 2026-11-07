from flask import Flask, render_template, request, Response, jsonify

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

@app.route("/submit-data", methods=["POST"])
def file_submit():
    file = request.files.get('data-file')

    if file is None:
        return bad_request("Nenhum arquivo selecionado")

    data_response = data.read_file(file)

    if data_response.data is None:
        return bad_request(data_response.text)

    _context.data = data_response.data

    return jsonify({"text": data_response.text})


def main():
    app.run(
        debug=True,
    )


if __name__ == '__main__':
    main()
