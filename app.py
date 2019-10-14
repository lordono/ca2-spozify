import os
from flask import Flask, escape, request, jsonify, current_app

from .spotify_fuzzy_music import FuzzyMusic

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')


@app.route('/find', methods=['POST'])
def find_top_music():

    fuzzyMusic = FuzzyMusic()
    content = request.json

    songs = fuzzyMusic.suggest_music(content['data'])
    songs.sort_values(by='musicScore', ascending=False, inplace=True)
    top_songs = songs[0:50]
    return jsonify(top_songs.to_dict('records'))
