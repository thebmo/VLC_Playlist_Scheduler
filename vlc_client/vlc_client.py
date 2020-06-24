import requests
import http.client
from urllib.parse import urljoin


# TODO 6.24.2020: remove teh conf stuff from where
# and implement proper config management
# should remove url params from client arguements.
# maybe make a master config yml file or something

# Config
base_url = 'http://127.0.0.1'
port = '8080'
url = "{}:{}".format(base_url, port)
status_endpoint = '/requests/status.json'
playlist_endpoint = '/requests/playlist.json'
status = urljoin(url, status_endpoint)


# returns a status of currently playing frmo your status endpoint
# {
#   "title": <string>,
#   "duration": <int>,
#   "current": <int>"]
# }
def get_status(status_url):
    json = get_response_json(status_url)
    return {
      "title": json["information"]["category"]["meta"]["filename"],
      "duration": json["length"],
      "current": json["time"]
    }


# returns a playlist of videos
# [{'duration': 8015, 'title': 'UCB_SEASON 1 disc 1.avi', 'id': '3'},
#  {'duration': 5345, 'title': 'UCB_SEASON 1 disc 2.avi', 'id': '4'}]
def get_playlist(playlist_url):
    playlist = []
    json = get_response_json(playlist_url)
    for child in json["children"]:
        if child["name"] == "Playlist":
            for subchild in child["children"]:
                playlist.append({
                    "title": subchild["name"],
                    "duration": subchild["duration"],
                    "id": subchild['id']
                })
            break
    return playlist


def get_response_json(url):
    # TODO 6.24.2020: get this pw out of here
    auth = requests.auth.HTTPBasicAuth('', 'pass')
    json = {}
    try:
        with requests.Session() as s:
            response = s.get(url, auth=auth)
            print(response.status_code)
            json = response.json()
    except:
        raise Exception("failed request: {}".format(url))
    return json
