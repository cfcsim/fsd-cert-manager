from flask import Flask, request, jsonify
from markupsafe import escape
import fsdcert
import logging
import hashlib
import json

token = "Wu21fJ0TpoDXbh95LRmCrqNP7in4ltU6"

app = Flask(__name__)
cert = fsdcert.create_cert()

@app.route('/whazzup.txt', methods=['GET']) 
def whazzupfile():
    return whazzup()

"""
API:
    Style: RESTful
    Path: /<method>
    Require param:
        token, callsign (public)
        password (method create & login)
        newpwd, newlevel (method change, min param 1, max param 2)
"""
def get_params(body, required_params=[]):
    global token
    required_params.append('token')
    try:
        params = json.loads(body)
    except:
        return None
    for param in required_params:
        if not param in params:
            app.logger.info("Miss param "+param)
            return None
    if not params['token'] == token:
        app.logger.info("Error token "+params['token'])
        return None
    return params

@app.route('/query/<callsign>', methods=['GET'])
def api_query(callsign):
    if not callsign in cert:
        return {'is_exist': False}
    return {'is_exist': True, 'level': cert[callsign]['level']}

@app.route('/create', methods=['POST'])
def api_create():
    params = get_params(request.get_data(), required_params=['callsign', 'password'])
    if not params:
        return {'message': 'Bad Request'}, 400
    if params['callsign'] in cert:
        return {'message': 'Conflict'}, 409
    cert[params['callsign']] = {'password': params['password'], 'level': 1}
    return {'message': 'OK'}

@app.route('/modify', methods=['POST'])
def api_modify():
    params = get_params(request.get_data(), required_params=['callsign'])
    if not params:
        return {'message': 'Bad Request'}, 400
    if not 'password' in params and not 'level' in params:
        return {'message': 'Bad Request'}, 400
    if not params['callsign'] in cert:
        return {'message': 'Not Found'}, 404
    newcert = {}
    if 'password' in params: newcert['password'] = params['password']
    if 'level' in params: newcert['level'] = params['level']
    cert[params['callsign']] = newcert
    return {'message': 'OK'}

@app.route('/delete/<callsign>', methods=['DELETE'])
def api_delete(callsign):
    if not get_params(request.get_data()):
        return {'message': 'Bad Request'}, 400
    if not callsign in cert:
        return {'message': 'Not Found'}, 404
    del cert[callsign]
    return {'message': 'OK'}

@app.route('/login', methods=['GET'])
def api_login():
    params = get_params(request.get_data(), required_params=['callsign', 'password'])
    if not params:
        return {'message': 'Bad Request'}, 400
    if not params['callsign'] in cert:
        return {'message': 'Not Found'}, 404
    d = cert[params['callsign']]
    rp = d['password']
    if rp == params['password'] or hashlib.new('md5', rp.encode()) == params['password']:
        return {'message': 'OK', 'level': d['level']}
    return {'message': 'Forbidden'}, 403

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.access')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
