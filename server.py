"""REST API"""
import json

import flask
import pandas
from flask import request

import database
import setting

app = flask.Flask(__name__)


@app.route('/take_schedule', methods=['GET'])
def take_schedule():
    return pandas.read_sql("SELECT * FROM schedule", database.DbSchedule().connection).to_json(orient='records')

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
