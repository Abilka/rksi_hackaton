"""REST API"""
import json

import flask
from flask import request

import database
import scheduler
import setting

app = flask.Flask(__name__)
schedule = scheduler.Schedule()


@app.route('/create_changed', methods=['GET'])
def create_changed():
    schedule.changed_needed()
    schedule.save_json()
    with open("Лист замен.json", 'r') as f:
        return json.dumps(f.read())


@app.route('/take_changed', methods=['GET'])
def send_changed():
    if schedule.changed is None:
        schedule.changed_needed()
    schedule.save_json()
    with open("Лист замен.json", 'r') as f:
        return json.dumps(f.read())


@app.route('/login', methods=['GET'])
def login():
    return {"result": database.Db().is_login(request.args['login'], request.args['password'])}


@app.route('/new_password', methods=['GET'])
def new_password():
    return {"result": database.Db().new_password(request.args['login'], request.args['password'])}


@app.route('/new_user', methods=['GET'])
def new_user():
    return {"result": database.Db().new_user(request.args['login'], request.args['password'], request.args['role'])}


@app.route('/get_user', methods=['GET'])
def get_user():
    return {"result": database.Db().get_users()}


@app.route('/get_role', methods=['GET'])
def get_role():
    return {"result": database.Db().get_role(request.args['login'])}




app.run(port=setting.SERVER_PORT, host="0.0.0.0")
# app.run(port=setting.SERVER_PORT)
