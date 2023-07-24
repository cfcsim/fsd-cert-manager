"""fsdapi

API:
    Style: RESTful
    Path: /<method>
    Require param:
        token, callsign (public)
        password (method create & login)
        newpwd, newlevel (method change, min param 1, max param 2)
"""
import hashlib
import json
import logging
import os
import sys

from flask import Flask, request, send_file

import fsdcert

token = "Wu21fJ0TpoDXbh95LRmCrqNP7in4ltU6"

app = Flask(__name__)
cert = fsdcert.cert()


@app.route("/whazzup.txt", methods=["GET"])
def whazzupfile():
    return send_file(os.path.join(sys.path[0], "whazzup.txt"))


def get_params(body, required_params=None):
    try:
        params = json.loads(body)
    except json.decoder.JSONDecodeError:
        return None
    if required_params:
        for param in required_params:
            if not param in params:
                return None
    if not params.get("token") == token:
        return None
    return params


@app.route("/query/<callsign>", methods=["GET"])
def api_query(callsign):
    if not callsign in cert:
        return {"is_exist": False}
    return {"is_exist": True, "level": cert[callsign]["level"]}


@app.route("/create", methods=["POST"])
def api_create():
    params = get_params(request.get_data(), required_params=["callsign", "password"])
    if not params:
        return {"message": "Bad Request"}, 400
    if params["callsign"] in cert:
        return {"message": "Conflict"}, 409
    cert[params["callsign"]] = {"password": params["password"], "level": 1}
    return {"message": "OK"}


@app.route("/modify", methods=["POST"])
def api_modify():
    params = get_params(request.get_data(), required_params=["callsign"])
    if not params:
        return {"message": "Bad Request"}, 400
    if not "password" in params and not "level" in params:
        return {"message": "Bad Request"}, 400
    if not params["callsign"] in cert:
        return {"message": "Not Found"}, 404
    newcert = {}
    if "password" in params:
        newcert["password"] = params["password"]
    if "level" in params:
        newcert["level"] = params["level"]
    cert[params["callsign"]] = newcert
    return {"message": "OK"}


@app.route("/delete/<callsign>", methods=["DELETE"])
def api_delete(callsign):
    if not get_params(request.get_data()):
        return {"message": "Bad Request"}, 400
    if not callsign in cert:
        return {"message": "Not Found"}, 404
    del cert[callsign]
    return {"message": "OK"}


@app.route("/login", methods=["GET"])
def api_login():
    params = get_params(request.get_data(), required_params=["callsign", "password"])
    if not params:
        return {"message": "Bad Request"}, 400
    if not params["callsign"] in cert:
        return {"message": "Not Found"}, 404
    cert_line = cert[params["callsign"]]
    right_password = cert_line["password"]
    if (
        right_password == params["password"]
        or hashlib.new("md5", right_password.encode()).hexdigest() == params["password"]
    ):
        return {"message": "OK", "level": cert_line["level"]}
    return {"message": "Forbidden"}, 403


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.access")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
