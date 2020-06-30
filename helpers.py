import datetime
import logging
import os
import yaml

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
