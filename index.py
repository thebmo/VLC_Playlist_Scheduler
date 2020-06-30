import datetime
from flask import Flask, jsonify, render_template
from helpers import elapsed_percent, ensure_logs_dir, human_readable_time, load_yaml, setup_logging
from vlc_client.vlc_client import VLCClient

app = Flask(__name__)
config = load_yaml('config.yaml')
ensure_logs_dir(config['LOGGING']['path'])

file = setup_logging(config['LOGGING']['path'])
app.logger.addHandler(file)
app.config['DEBUG'] = True

vlc = VLCClient(config['VLC'])

@app.route('/')
def index():
    # TODO 6.25.2020: scrape out the schedule builder into a helper method
    # TODO 6.26.2020: Throw a 404 if vlc is not running instead of breaking app
    original_playlist = vlc.get_playlist()
    current = vlc.get_status()

    # re-order playlist with current item on top
    curr_index = 0
    for i, item in enumerate(original_playlist):
        if item['title'] == current['title']:
            curr_index = i
            break
    playlist = original_playlist[curr_index:] + original_playlist[:curr_index]

    # update the currently playing video witha dditional properties
    current['readable_elapsed'] = human_readable_time(current['elapsed'])
    current['readable_duration'] = human_readable_time(current['duration'])
    current['progress_percent'] = elapsed_percent(
                                    current['elapsed'],
                                    current['duration'])

    # calculate deltas for air_date and insert into playlist
    running_time = datetime.datetime.now()
    for i, item in enumerate(playlist):
        # do nothing on first pass through
        if i == 1:
            # The second item in the playlist's air_date is calculated
            # by subtracting the elapsed time of the current track from its
            # duration
            running_time += datetime.timedelta(
                seconds=current['duration'] - current['elapsed'])
        elif i > 1:
            running_time += datetime.timedelta(seconds=item['duration'])

        # Add additional properties into playlist item
        item['air_date'] = str(running_time).split('.')[0]
        item['readable_duration'] = human_readable_time(item['duration'])

    # return jsonify(playlist)
    return render_template('index.html',
                            current=current,
                            playlist=playlist,
                            ui=config['UI'])


# Returns the currently playing video with basic
# stats as a json object
@app.route('/current')
def current():
    return jsonify(vlc.get_status())


@app.route('/playlist')
def playlist():
    # returns a json list of vidoes with
    #   title
    #   duration
    #   expected air time | missing right nowm maybe should be part
    #     of the schedule
    return jsonify(vlc.get_playlist())
