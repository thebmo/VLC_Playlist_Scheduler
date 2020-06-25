import datetime
from flask import Flask, jsonify
import vlc_client.vlc_client as VLC


app = Flask(__name__)
# TODO 6.24.2020: I Think this is where we set env vars.
# write a config loader class to handle this safely.


@app.route('/')
def index():
    # TODO 6.25.2020: scrape out the schedule builder into a helper method
    original_playlist = VLC.get_playlist('http://127.0.0.1:8080/requests/playlist.json')
    current = VLC.get_status('http://127.0.0.1:8080/requests/status.json')

    # re-order playlist with current item on top
    curr_index = 0
    for i, item in enumerate(original_playlist):
        if item['title'] == current['title']:
            curr_index = i
            break
    playlist = original_playlist[curr_index:] + original_playlist[:curr_index]

    # calculate deltas and insert into playlist
    running_time = datetime.datetime.now()
    for i, item in enumerate(playlist):
        # do nothing on first pass through
        if i == 1:
            # first item we want to diff on the current position
            # of what is currently playing
            running_time += datetime.timedelta(
                seconds=current['duration'] - current['elapsed'])
        elif i > 1:
            running_time += datetime.timedelta(seconds=item['duration'])

        item['air_date'] = str(running_time)

    return jsonify(playlist)


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
