import json
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/hello_world", methods=('GET',))
def hello():
    return jsonify("Hello world!")


@app.route("/api/config", methods=('GET',))
def get_config():
    with open('data/config.json', 'r') as f:
        config = json.load(f)

    return jsonify(config)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
