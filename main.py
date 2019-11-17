import json
import os

from flask import Flask, jsonify, request
from contants import default_config, id_to_file_name

app = Flask(__name__)


@app.route("/api/ping", methods=('GET',))
def ping():
    message = request.args.get("message", None)
    response = default_config.copy()

    if message:
        response['data'] = {
            "message": message
        }
        response['success'] = True
        response['status'] = 200
    else:
        response['success'] = False
        response['status'] = 501
        response['error'] = 'Missing parameter <message>'

    return jsonify(response)


@app.route("/api/config", methods=('GET',))
def get_config():
    response = default_config.copy()

    with open('data/config.json', 'r') as f:
        response['data'] = json.load(f)
        response['data']['api']['server'] = request.host_url[:-1]
        response['success'] = True
        response['status'] = 200

    return jsonify(response)


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


@app.route("/api/login", methods=('POST',))
def login():
    response = default_config.copy()
    data = json.loads(request.data)
    login_name = data.get("login", None)
    password = data.get("password", None)

    if not login_name:
        response['error'] = "required field <login> in request body"
    else:
        with open("data/login.json", 'r') as f:
            login_data = json.load(f)
            user = None

            for item in login_data:
                if item['login'] == login_name:
                    user = item
                    break

            if not user:
                response['error'] = "user with this login doesn't registered"
            elif user['password'] == password:
                response['success'] = True
                response['status'] = 200
                response['data'] = {
                    'id': user['id'],
                    'token': user['token']
                }
            else:
                response['error'] = "password error"

    return jsonify(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
