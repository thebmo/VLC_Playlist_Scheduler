import datetime
from flask import Flask, jsonify, redirect, render_template, url_for
from helpers import build_schedule, elapsed_percent, ensure_logs_dir, human_readable_time, load_yaml, setup_logging
from vlc_client.vlc_client import VLCClient

app = Flask(__name__)
config = load_yaml('config.yaml')
ensure_logs_dir(config['LOGGING']['path'])

file = setup_logging(config['LOGGING']['path'])
app.logger.addHandler(file)

vlc = VLCClient(config['VLC'])
schedule = {}

@app.route('/')
def index():
    # TODO 6.25.2020: scrape out the schedule builder into a helper method
    # TODO 6.26.2020: Throw a 404 if vlc is not running instead of breaking app
    schedule = vlc.get_playlist()
    current = vlc.get_status()
    playlist = build_schedule(current, schedule)
    return render_template('index.html',
                            current=current,
                            playlist=playlist,
                            ui=config['UI'])


# Returns the currently playing video with basic
# stats as a json object
@app.route('/current')
def current():
    if app.env == 'development':
        return jsonify(vlc.get_status())
    else:
        return redirect(url_for('index'))


@app.route('/playlist')
def playlist():
    # returns a json list of vidoes with
    #   title
    #   duration
    #   expected air time | missing right nowm maybe should be part
    #     of the schedule
    if app.env == 'development':
        return jsonify(vlc.get_playlist())
    else:
        return redirect(url_for('index'))
