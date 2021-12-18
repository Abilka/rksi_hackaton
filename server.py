"""REST API"""
import json

import flask

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

app.run(port=setting.SERVER_PORT, host="0.0.0.0")