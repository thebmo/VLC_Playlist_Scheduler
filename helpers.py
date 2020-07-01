import datetime
import logging
import os
import yaml


def build_schedule(current, original_playlist):
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

    return playlist


def ensure_logs_dir(log_dir):
    try:
        os.makedirs(log_dir, exist_ok=True) # Python>3.2
    except TypeError:
        try:
            os.makedirs(log_dir)
        except OSError as err: # Python >2.5
            if err.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

def elapsed_percent(elapsed, duration):
    return int((float(elapsed) / float(duration)) * 100)


def human_readable_time(seconds):
    delta = datetime.timedelta(seconds=seconds)
    return (datetime.datetime(1900,1,1) + delta).strftime("%H:%M:%S").split('.')[0]


def load_yaml(file_path):
    with open(file_path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def setup_logging(logging_path):
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    file = logging.FileHandler("{}/{}.log".format(
            logging_path,
            datetime.datetime.now().date()))
    formatter = logging.Formatter(logFormatStr,'%m/%b/%Y %H:%M:%S')
    file.setFormatter(formatter)
    file.setLevel(logging.INFO)

    return file
