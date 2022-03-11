from flask import Flask, request, jsonify
from markupsafe import escape
import fsdcert
import logging
import json

token = "Paste token here"

app = Flask(__name__)

@app.route('/whazzup.txt', methods=['GET']) 
def whazzupfile():
    return whazzup()

"""
API:
    Style: RESTful
    Path: POST /api/<method>
    Require param:
        token, callsign (public)
        password (method create & login)
        newpwd, newpriv (method change, min param 1, max param 2)
    'state' param explain:
        See list 'msgs'.
"""
msgs = [
    'OK',
    'Invaild JSON body',
    'Missing param',
    'Token wrong',
    'Callsign does not exist',
    'Callsign already exist',
    'API method not found'
]

def buildresult(state, moremsg='', params={}):
    global msgs
    params['state'] = state
    if state > 0:
        params['msg'] = msgs[state]+moremsg
    return jsonify(params)

@app.route('/api/<method>', methods=['POST']) 
def api(method):
    method = escape(method)
    try:
        params = json.loads(request.get_data())
    except json.decoder.JSONDecodeError:
        return buildresult(1), 400
    if not params.get("token") == token:
        return buildresult(3), 403
    elif not "callsign" in params:
        return buildresult(2, moremsg=': callsign'), 400
    if method == "query":
        result = fsdcert.query(params.get('callsign'))
        if type(result) == int:
            return buildresult(0, params={'is_exist': True, 'priv': result})
        else:
            return buildresult(0, params={'is_exist': False}) 
    elif method == "modify":
        if not 'priv' in params and not 'password' in params:
            return buildresult(2, moremsg=': priv or(and) password'), 400
        if not fsdcert.modify(params.get('callsign'), newpriv=params.get('priv'), newpwd=params.get('password')):
            return buildresult(4)
        else:
            return buildresult(0)
    if not "password" in params and method in ['create', 'login']:
        return buildresult(2, moremsg=': password'), 400
    if method == "create":
        if not fsdcert.create(params.get("callsign"), params.get("password")):
            return buildresult(5)
    elif method == "login":
        result = fsdcert.login(params.get("callsign"), params.get("password"))
        if type(result) == int:
            return buildresult(0, params={'success': True, 'priv': result})
        else:
            return buildresult(0, params={'success': False})
    else:
        return buildresult(6), 404
    return buildresult(0)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
fsdcert.logger = app.logger
