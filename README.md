# VLC_Playlist_Scheduler #
A small web app to create a servable schedule of airtimes for videos in a VLC playlist

* install flask with `pip3 install Flask`
* set flask env `export FLASK_APP=index.py`
* run the app `flask run`


#### VLC docs ####
* VLC Configuration - https://wiki.videolan.org/Documentation:Modules/http_intf/
* HTTP requests (SAOP) - https://wiki.videolan.org/VLC_HTTP_requests/
* how to enable http interface - https://hobbyistsoftware.com/vlcsetup-win-manual

exaple requests:
* http://127.0.0.1:8080/requests/playlist.xml
* http://127.0.0.1:8080/requests/status.xml

#### Work flow ####
* Scrape playlist - https://docs.google.com/document/d/1Eabyw_ym479h_pZC_sPMmstX5NClywcAWlqUdzFSECg/edit

* parse to decent format (parser.py)
* fetch what is playing (with current duration in seconds)
* figure out where in the playlist it is
* calculate when each item will play based on what is currently playing (EST or whatever)
* write to UI

#### todo ####
* build flask app
* build parser
* build scheduler
* set up cron job to look at the diff of source and in memory playlists
