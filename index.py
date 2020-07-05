import datetime
from flask import Flask, jsonify, redirect, render_template, url_for
from helpers import(build_schedule, elapsed_percent, ensure_logs_dir,
human_readable_time, load_yaml, schedule_expired, setup_logging)
from vlc_client.vlc_client import VLCClient

app = Flask(__name__)
config = load_yaml('config.yaml')

ensure_logs_dir(config['LOGGING']['path'])
log_file = setup_logging(config['LOGGING']['path'])
app.logger.addHandler(log_file)

vlc = VLCClient(config['VLC'])
SCHEDULE = {
    "exp": datetime.datetime.now(),
    "playlist": {},
    "current": {}
 }

@app.route('/')
def index():
    # TODO 6.26.2020: Throw a 404 if vlc is not running instead of breaking app

    # rebuild the schedule if the cache has expired
    if schedule_expired(SCHEDULE):
        try:
            current = vlc.get_status()
            playlist = vlc.get_playlist()
            SCHEDULE.clear()
            SCHEDULE.update(build_schedule(current,
                                           playlist,
                                           config['VLC']['cache_expiration']))
        except Exception as e:
            print(e)

    if app.debug:
        ("cache expires at: {}".format(SCHEDULE['exp']))

    return render_template('index.html',
                            current=SCHEDULE['current'],
                            playlist=SCHEDULE['playlist'],
                            ui=config['UI'],
                            refresh=config['VLC']['cache_expiration'])


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
