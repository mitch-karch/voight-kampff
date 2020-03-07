from discord import Embed

import logging
import json
import sys
import os.path
import re
import urllib.parse

import spotipy
import spotipy.util as util

class SpotifyWrapper:
    def __init__(self):
        self.token = None

    def refresh_token(self, username):
        self.username = username

        if os.path.isfile("spotify.json"):
            with open('spotify.json') as f:
                self.token = json.load(f)
                return self.token
        scope = 'playlist-modify-public user-library-read user-library-modify user-read-private user-follow-read playlist-read-collaborative'
        token = util.prompt_for_user_token(username, scope)
        if token:
            with open('spotify.json', 'w') as f:
                json.dump(token, f)
            self.token = token
            return token
        raise Exception("error getting token")

    # We can generalize the paging logic here.
    def get_or_create_playlist(self, name):
        sp = spotipy.Spotify(auth=self.token)
        sp.trace = False

        page = 0
        while True:
            playlists = sp.current_user_playlists(limit=50, offset=page*50)
            if len(playlists['items']) == 0:
                break
            for pl in playlists['items']:
                if pl['name'] == name:
                    return pl
            page += 1

        user = sp.current_user()
        username = user['display_name']
        return sp.user_playlist_create(username, name, description=name)

    def add_track_to_playlist(self, playlist_id, track_ids):
        sp = spotipy.Spotify(auth=self.token)
        sp.trace = False

        user = sp.current_user()
        username = user['display_name']
        results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
        print(results)

def find_all_urls(string):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)

class SpotifyBot:
    def __init__(self):
        self.log = logging.getLogger('spotify')
        self.sc = SpotifyWrapper()
        self.playlistName = 'murderoke'

    def initialize(self):
        self.token = self.sc.refresh_token('')
        self.log.info("authenticated")

        self.pl = self.sc.get_or_create_playlist(self.playlistName)
        self.log.info("found playlist", self.pl)

    def on_message(self, channel, message, dry=False):
        urls = find_all_urls(message)
        if len(urls) == 0:
            return

        for url in urls:
            self.log.info("checking %s", url)
            self.on_url(channel, urllib.parse.urlparse(url), dry)

    def on_url(self, channel, url, dry):
        if not url.netloc in ['open.spotify.com']:
            return

        self.log.info("spotify %s", url.path)

        path = [i for i in url.path.split("/") if i]
        if len(path) != 2:
            return

        if path[0] == 'track':
            track_id = path[1]
            self.log.info("track %s", track_id)
            if not dry:
                self.sc.add_track_to_playlist(self.pl['id'], [ track_id ])

        # TODO Albums and artists? Sample their tracks?

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    s = SpotifyBot()
    s.initialize()
    s.on_message('test', 'https://open.spotify.com/track/0vj7w2ykn6IwOdNk4ggd2g?si=1UpQCzFsSKS17v5gJIXwVQ', dry=True)
    s.on_message('test', 'some text https://open.spotify.com/track/0vj7w2ykn6IwOdNk4ggd2g?si=1UpQCzFsSKS17v5gJIXwVQ around things', dry=True)
