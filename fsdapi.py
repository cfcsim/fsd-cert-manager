from flask import Flask, request
from markupsafe import escape
from fsdcert import *
import json

token = "Paste token here"

app = Flask(__name__) 
logger = app.logger

@app.route('/whazzup.txt', methods=['GET']) 
def whazzupfile():
    return whazzup()

@app.route('/api/<path>', methods=['POST']) 
def api(path):
    path = escape(path)
    try:
        list = json.loads(request.get_data())
    except json.decoder.JSONDecodeError:
        return { "status": 400, "error": "Bad Request: Only accept JSON body" }, 400
    if not list.get("token") == token:
        return { "status": 403, "error": "Forbidden: Token incorrect" }, 403
    elif not "name" in list:
        return { "status": 400, "error": "Bad Request: Missing name" }, 400
    if path == "query":
        result = query(list.get("name"))
    elif path == "changeauth":
        if not "auth" in list:
            return { "status": 400, "error": "Bad Request: Missing auth" }, 400
        result = changeauth(list.get("name"), list.get("auth"))
    if 'result' in dir(): return result, result['status']
    if not "password" in list:
        return { "status": 400, "error": "Bad Request: Missing password" }, 400
    if path == "create":
        result = create(list.get("name"), list.get("password"))
    elif path == "changepwd":
        result = changepwd(list.get("name"), list.get("password"))
    elif path == "auth":
        result = checkauth(list.get("name"), list.get("password"))
    else:
        result = { "status": 404, "error": "Not Found: Invaild API method" }
    return result, result['status']
