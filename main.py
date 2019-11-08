import json
import os

from flask import Flask, jsonify, request
from contants import default_config, id_to_file_name

app = Flask(__name__)


@app.route("/api/hello_world", methods=('GET',))
def hello():
    return jsonify("Hello world!")


@app.route("/api/config", methods=('GET',))
def get_config():
    with open('data/config.json', 'r') as f:
        config = json.load(f)

    return jsonify(config)


@app.route("/api/country", methods=('GET',))
def get_country():
    country_id = request.args.get("id", None)
    config = default_config.copy()

    path_to_file = 'data/countries/{}'.format(id_to_file_name.get(country_id.lower()))
    is_json_exist = os.path.isfile(path_to_file)

    if is_json_exist:
        with open(path_to_file, 'r') as f:
            config = json.load(f)
    else:
        config["status"] = 404
        config["error"] = "Can't find requested data"

    if not country_id:
        config["status"] = 404
        config["error"] = "Missing parameter [id]"

    return jsonify(config)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
