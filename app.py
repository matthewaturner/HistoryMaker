import string
import random
import json
from typing import Tuple, Dict

import app
import spotify.sync as spotify

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    config = load_config()
    SPOTIFY_CLIENT = spotify.Client(config.spotify.client_id, config.spotify.client_secret)

    APP = app.Flask(__name__)
    APP.config.from_mapping({'spotify_client': SPOTIFY_CLIENT})

    REDIRECT_URI: str = 'http://localhost:8888/spotify/callback'

    OAUTH2_SCOPES: Tuple[str] = ('user-modify-playback-state', 'user-read-currently-playing', 'user-read-playback-state')
    OAUTH2: spotify.OAuth2 = spotify.OAuth2(SPOTIFY_CLIENT.id, REDIRECT_URI, scopes=OAUTH2_SCOPES)

    SPOTIFY_USERS: Dict[str, spotify.User] = {}

# Flask routes

@APP.route('/spotify/callback')
def spotify_callback():
    try:
        code = app.request.args['code']
    except KeyError:
        return app.redirect('/spotify/failed')
    else:
        key = ''.join(random.choice(string.ascii_uppercase) for _ in range(16))
        SPOTIFY_USERS[key] = spotify.User.from_code(
            SPOTIFY_CLIENT,
            code,
            redirect_uri=REDIRECT_URI,
            refresh=True
        )

        app.session['spotify_user_id'] = key

    return app.redirect('/')

@APP.route('/spotify/failed')
def spotify_failed():
    app.session.pop('spotify_user_id', None)
    return 'Failed to authenticate with Spotify.'

@APP.route('/')
@APP.route('/index')
def index():
    try:
        return repr(SPOTIFY_USERS[app.session['spotify_user_id']])
    except KeyError:
        return app.redirect(OAUTH2.url)

if __name__ == '__main__':
    APP.run('127.0.0.1', port=8888, debug=False)