import datetime
import logging
import os
import yaml


def build_schedule(current, original_playlist, expiration):
    # re-order playlist with current item on top
    curr_index = 0
    for i, item in enumerate(original_playlist):
        if item['title'] == current['title']:
            curr_index = i
            break
    playlist = original_playlist[curr_index:] + original_playlist[:curr_index]

    # update the currently playing video witha dditional properties
    # for the template. see "templates/index.py" for useage
    current['readable_elapsed'] = human_readable_time(current['elapsed'])
    current['readable_duration'] = human_readable_time(current['duration'])
    current['progress_percent'] = elapsed_percent(
                                    current['elapsed'],
                                    current['duration'])

    # calculate deltas for air_date and insert into playlist
    # uses UTC time and format it to client timezone on the frontend
    now = datetime.datetime.utcnow()
    running_time = 0
    for i, item in enumerate(playlist):
        if i == 0:
            # first pass, running time is how much of the current item
            # has been played
            item['air_date'] = now
            running_time += current['duration'] - current['elapsed']
        else:
            item['air_date'] = now + datetime.timedelta(seconds=running_time)
            running_time += item['duration']

        # Add additional properties into playlist item for the template
        item['readable_duration'] = human_readable_time(item['duration'])

    return { "current": current,
             "playlist": playlist,
             "exp": set_expiration(expiration) }


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


def schedule_expired(schedule):
    return  datetime.datetime.now() > schedule['exp']


def set_expiration(duration):
    return datetime.datetime.now() + datetime.timedelta(seconds=duration)


def setup_logging(logging_path):
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    file = logging.FileHandler("{}/{}.log".format(
            logging_path,
            datetime.datetime.now().date()))
    formatter = logging.Formatter(logFormatStr,'%m/%b/%Y %H:%M:%S')
    file.setFormatter(formatter)
    file.setLevel(logging.INFO)

    return file
