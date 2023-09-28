from flask import Flask, request, render_template, jsonify, redirect, url_for
import json
import pickle as pkl
import http.client

from music_rex.music_rex import MusicRex
from music_rex.machine_learning import get_similar_songs
from collections import namedtuple

import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import requests

Song = namedtuple("Song", ["artist", "title"])
app = Flask(__name__, static_url_path='/static')
mr = MusicRex()

token = 'BQB9arsfDX3fWRrTMQ2V3I0xB1wR4Os0l1nsEv0tW8_bUDd2xlmSIUCUVivk_b9OSp_1afhnvIlBKTculEyaU7iLcTH7uRsyBN97tcdLxrQNfrHRAWN8va8WI789lOlqgZKkzk-W9SiuqyW54lYIPxCkpvgmflY5wizPO4gq4crMqPDDlfmttpn6cMs1wORAtU7DPUPkk-VpVz2HK6F4JMTxCKvq52WigERlgvmH4u3GIkri4XqgxNGU3cq22QLhG1GVVIrT4QJUQ-MgKYvQcVcvhG-y';
CLIENT_ID='5f9548cc54f242bb97c58c5dfeb884c5'
CLIENT_SECRET='03ebdb028ed6454ba33102e925f1fcc1'
USER_ID = '317u5f5phywzysmnov6x6tppkrxq'

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=["POST"])
def submit():
    song_title = request.form.get('songTitle')
    artist = request.form.get('artist')
    track = mr.get_top_track(artist, song_title)
    features = mr.get_audio_track_features(track['id'])
    success = (( features is not None) and len(features) > 0)

    return jsonify(features), (http.client.OK if success else http.client.BAD_REQUEST)

@app.route('/lyrics', methods=["GET"])
def lyrics():
    song_title = request.args.get('song_title')
    artist = request.args.get('artist')
    lyrics = mr.get_lyrics(artist, song_title)
    success = (( lyrics is not None) and len(lyrics) > 0)
    return jsonify(lyrics), (http.client.OK if success else http.client.BAD_REQUEST)

@app.route('/playlist', methods=["POST"])
def playlist():
    args = request.get_json(force=True)
    lyrics = args["lyrics"]
    features = args["features"]
    recommendations = get_similar_songs(features, lyrics)

    tracksUri = []
    final_result_dictionary = recommendations
    for i in range(len(final_result_dictionary['playlist'])-1):
        artist = final_result_dictionary['playlist'][i][0]
        track = final_result_dictionary['playlist'][i][1]

        results = spotify.search(q="artist:" + artist + " track:" + track, type="track")
        items = results['tracks']["items"]
        if len(items)>0:
            print(items[0]['uri'])
            tracksUri.append(items[0]['uri'])
    # tao playlist
    endpoint_url = "https://api.spotify.com/v1/users/{}/playlists".format(USER_ID)
    request_body = json.dumps({
            "name": "Chúc bạn nghe nhạc zui zẻ :>",
            "description": "Khum",
            "public": True
            })
    response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                            "Authorization":"Bearer {}".format(token)})

    #add bai hat
    playlist_id = response.json()['id']
    endpoint_url = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(playlist_id, ','.join(tracksUri))
    response_final = requests.post(url = endpoint_url,headers={"Content-Type":"application/json", 
                            "Authorization":"Bearer {}".format(token)})
    return jsonify('https://open.spotify.com/embed/playlist/{}?utm_source=generator&theme=0'.format(playlist_id)), (http.client.OK)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True, passthrough_errors=False)
