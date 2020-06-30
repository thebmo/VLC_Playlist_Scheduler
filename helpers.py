import datetime
import yaml

def elapsed_percent(elapsed, duration):
    return int((float(elapsed) / float(duration)) * 100)


def human_readable_time(seconds):
    delta = datetime.timedelta(seconds=seconds)
    return (datetime.datetime(1900,1,1) + delta).strftime("%H:%M:%S").split('.')[0]


def load_yaml(file_path):
    with open(file_path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)
