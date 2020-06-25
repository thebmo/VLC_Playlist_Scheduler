# VLC_Playlist_Scheduler #
A small web app to create a servable schedule of airtimes for videos in a VLC playlist

**Local Setup Steps:**
* install flask with `pip3 install Flask`
* set flask env `export FLASK_APP=index.py`
* run the app `flask run`
* app should be running on: `http://127.0.0.1:5000/`
* make sure VLC is running with an http interface and password set (user optional)

#### VLC Docs ####
* VLC Configuration - https://wiki.videolan.org/Documentation:Modules/http_intf/
* HTTP requests (SAOP) - https://wiki.videolan.org/VLC_HTTP_requests/
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
