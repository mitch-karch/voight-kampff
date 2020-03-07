from discord import Embed

import logging
import json
import sys
import os.path
import re
import requests
import urllib.parse

import spotipy
import spotipy.util as util

class SpotifyWrapper:
    def __init__(self):
        self.log = logging.getLogger('spotify')
        self.token = None

    def read_auth(self, fn):
        if os.path.isfile(fn):
            with open(fn) as f:
                return json.load(f)
        return None

    def write_auth(self, fn, auth):
        with open(fn, 'w') as f:
            json.dump(auth, f)

    def refresh_token(self):
        self.auth = self.read_auth("spotify.json")
        if not self.auth:
            raise Exception("missing initial spotify.json")

        self.username = self.auth['username']

        if 'token' in self.auth:
            self.token = self.auth['token']
            return self.token

        scope = 'playlist-modify-public playlist-modify-private user-library-read user-library-modify user-read-private user-follow-read playlist-read-collaborative'
        self.token = util.prompt_for_user_token(self.username, scope,
                                                client_id=self.auth['client_id'],
                                                client_secret=self.auth['client_secret'],
                                                redirect_uri=self.auth['redirect_uri'])
        if self.token:
            self.auth['token'] = self.token
            self.write_auth('spotify.json', self.auth)
            return self.token

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
        self.log.info(results)

def find_all_urls(string):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)

class SpotifyBot:
    def __init__(self):
        self.log = logging.getLogger('spotify')
        self.sc = SpotifyWrapper()
        self.playlistName = 'murderoke'

    def initialize(self):
        self.sc.refresh_token()
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
        if url.netloc in ['open.spotify.com']:
            self.on_spotify(channel, url, dry)
        if url.netloc in ['www.youtube.com', 'youtu.be']:
            self.on_youtube(channel, url, dry)

    def on_spotify(self, channel, url, dry):
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

    def on_youtube(self, channel, url, dry):
        video_id = self.get_youtube_id(url)
        if video_id:
            self.log.info("youtube video %s", video_id)
            info_url = 'https://www.youtube.com/get_video_info?video_id=%s' % video_id
            raw = requests.get(info_url).text
            info = urllib.parse.parse_qs(raw)
            if 'player_response' in info:
                info = json.loads(info['player_response'][0])
            if 'videoDetails' in info:
                info = info['videoDetails']
            if 'title' in info:
                title = info['title']
                self.log.info("youtube %s", title)

    def get_youtube_id(self, url):
        # TODO Check that this is a good ID?
        query = urllib.parse.parse_qs(url.query)
        video_id = None
        if 'v' in query and len(query['v']) == 1:
            return query['v'][0]
        return url.path[1:]

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    s = SpotifyBot()
    s.initialize()
    s.on_message('test', 'https://open.spotify.com/track/0vj7w2ykn6IwOdNk4ggd2g?si=1UpQCzFsSKS17v5gJIXwVQ', dry=True)
    s.on_message('test', 'some text https://open.spotify.com/track/0vj7w2ykn6IwOdNk4ggd2g?si=1UpQCzFsSKS17v5gJIXwVQ around things', dry=True)
    s.on_message('test', 'https://youtu.be/ijAYN9zVnwg', dry=True)
    s.on_message('test', 'https://www.youtube.com/watch?v=P5mtclwloEQ', dry=True)
