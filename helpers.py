import datetime

def human_readable_time(seconds):
    delta = datetime.timedelta(seconds=seconds)
    return (datetime.datetime(1900,1,1) + delta).strftime("%H:%M:%S").split('.')[0]


def elapsed_percent(elapsed, duration):
    return int((float(elapsed) / float(duration)) * 100)
