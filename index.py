import datetime
from flask import Flask, jsonify
import vlc_client.vlc_client as VLC

app = Flask(__name__)
# TODO 6.24.2020: I Think this is where we set env vars.
# write a config loader class to handle this safely.


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
    return jsonify(
        VLC.get_status('http://127.0.0.1:8080/requests/status.json'))


@app.route('/playlist')
def playlist():
    # returns a json list of vidoes with
    #   title
    #   duration
    #   expected air time | missing right nowm maybe should be part
    #     of the schedule
    return jsonify(
        VLC.get_playlist('http://127.0.0.1:8080/requests/playlist.json'))
