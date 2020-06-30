import requests
import http.client
from urllib.parse import urljoin


# TODO 6.25.2020: Handle duration -1 in playlist and status

# usage
# client = VLCClient([Dictionarion]config)
class VLCClient(object):
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.user = config['user'] if config['user'] != None else ''
        self.password = config['pass'] if config['pass'] != None else ''
        self.status_url = '/requests/status.json'
        self.playlist_url = '/requests/playlist.json'


    def get_url(self, endpoint):
        url = "{}:{}".format(self.host, self.port)
        return urljoin(url, endpoint)


    # returns a status of currently playing frmo your status endpoint
    # {
    #   "title": <string>,
    #   "duration": <int>,
    #   "elapsed": <int>"]
    # }
    def get_status(self):
        json = self.get_response_json(self.status_url)
        meta = json["information"]["category"]["meta"]
        title = meta["title"] if "title" in meta else meta["filename"]
        return {
          "title": title,
          "duration": json["length"],
          "elapsed": json["time"]
        }


    # returns a playlist of videos
    # [{'duration': 8015, 'title': 'UCB_SEASON 1 disc 1.avi', 'id': '3'},
    #  {'duration': 5345, 'title': 'UCB_SEASON 1 disc 2.avi', 'id': '4'}]
    def get_playlist(self):
        playlist = []
        json = self.get_response_json(self.playlist_url)
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


    def get_response_json(self, endpoint):
        auth = requests.auth.HTTPBasicAuth(self.user, self.password)
        json = {}
        url = self.get_url(endpoint)
        try:
            with requests.Session() as s:
                response = s.get(url, auth=auth)
                json = response.json()
        except:
            raise Exception("failed request: {}".format(url))
        return json
