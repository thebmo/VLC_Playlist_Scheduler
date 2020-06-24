import requests
import http.client
from urllib.parse import urljoin


## TODO 6.24.2020: remove teh conf stuff from where
# Config
base_url = 'http://127.0.0.1'
port = '8080'
url = "{}:{}".format(base_url, port)
status_endpoint = '/requests/status.json'
playlist_endpoint = '/requests/playlist.json'

status = urljoin(url, status_endpoint)




def get_status(status_url):
    json = {}
    try:
        response = make_request(status_url)
        json = response.json()
    except:
        raise Exception("failed to get status: {}".format(status_url))
    return {
      "title": json["information"]["category"]["meta"]["filename"],
      "duration": json["length"],
      "current": json["time"]
    }


def make_request(url):
    # TODO 6.24.2020: get this pw out of here
    auth = requests.auth.HTTPBasicAuth('', 'pass')
    response = requests.get(url, auth=auth)
    return response
