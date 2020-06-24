import datetime
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():

    # Get whats playing
    # Get the current playlist
    # Adjust list

    return 'this is the sechedule'


# Returns the currently playing video with basic
# stats as a json object
@app.route('/current')
def current():
    # should return json with
    #   title
    #   total duration (seconds)
    #   elapsed time (seconds)
    # maybe this should be back channel to prevent Ddos?
    resp = {
        "title": "test title",
        "duration": 3600,
        "elapsed": 1800
    }
    return jsonify(resp)


@app.route('/playlist')
def playlist():
    # returns a json list of vidoes with
    #   title
    #   duration
    #   expected air time
    resp = [{
        "title": "test title",
        "duration": 3600,
        "air_date": datetime.datetime.now()
    }]
    return jsonify(resp)
