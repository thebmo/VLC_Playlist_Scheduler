# VLC_Playlist_Scheduler #
A small web app to create a servable schedule of airtimes for videos in a VLC playlist

**Local Setup Steps and Dependencies:**
* **DEPENDENCY** install flask with `pip3 install Flask`
* **DEPENDENCY** install pyyaml with `pip3 install pyyaml`
* **DEPENDENCY** install requests with `pip3 install requests`
* **DEPENDENCY** install Flask-Moment with `pip3 install Flask-Moment`
* set flask app envar `export FLASK_APP=index.py`
* create/rename and setup `config.yaml` file (see `example.config.yaml`)
* run the app `flask run --host 0.0.0.0`
* app should be running on: `http://127.0.0.1:5000/`
* make sure VLC is running with an http interface and password set (user optional)

#### VLC Docs ####
* VLC Configuration - https://wiki.videolan.org/Documentation:Modules/http_intf/
* HTTP requests (SOAP/JSON) - https://wiki.videolan.org/VLC_HTTP_requests/
* how to enable http interface - https://hobbyistsoftware.com/vlcsetup-win-manual

**Example Requests:**
* http://127.0.0.1:8080/requests/playlist.json
* http://127.0.0.1:8080/requests/status.json

#### Work Flow ####
* Scrape playlist
* parse to decent format (parser.py)
* fetch what is playing (with current duration in seconds)
* figure out where in the playlist it is
* calculate when each item will play based on what is currently playing (EST or whatever)
* write to UI

#### Todo ####
* build flask app
* build parser
* build scheduler
* set up cron job to look at the diff of source and in memory playlists
* dockerize
* support webhooks (like discord!)


#### Screen Shot ####
![screenshot](https://github.com/thebmo/VLC_Playlist_Scheduler/blob/master/screen_shot.png)
