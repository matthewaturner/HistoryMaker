import asyncio
import json
import aiohttp
from aiohttp import web
from aiohttp.web import AppRunner, TCPSite
from contextvars import ContextVar
from urllib.parse import urlencode

def load_config() -> dict:
    with open('config.json', 'r') as f:
        return json.load(f)

config: dict = load_config()
CLIENT_ID: str = config['spotify']['client_id']
CLIENT_SECRET: str = config['spotify']['client_secret']
REDIRECT_URI: str = 'http://localhost:8080/spotify/callback'
SCOPE: str = 'user-library-read'  # Add additional scopes as needed

# Define a context variable to hold the access token
ACCESS_TOKEN: ContextVar[str] = ContextVar("spotify_access_token")

async def login(request):
    # Redirect the user to Spotify's authorization endpoint
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': SCOPE,
        'redirect_uri': REDIRECT_URI
    }
    auth_url = 'https://accounts.spotify.com/authorize?' + urlencode(params)
    return web.HTTPFound(auth_url)

async def callback(request):
    authorization_code = request.query.get('code')
    if authorization_code:
        # Exchange authorization code for access token
        async with aiohttp.ClientSession() as session:
            payload = {
                'grant_type': 'authorization_code',
                'code': authorization_code,
                'redirect_uri': REDIRECT_URI,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET
            }
            async with session.post('https://accounts.spotify.com/api/token', data=payload) as response:
                data = await response.json()
                access_token = data.get('access_token')
                ACCESS_TOKEN.set(access_token)
                return web.Response(text="Successfully logged in with Spotify!")
    else:
        return web.Response(text="Authorization code not found")

async def get_user_tracks(request):
    access_token = ACCESS_TOKEN.get()
    if access_token:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.spotify.com/v1/me/tracks', headers=headers) as response:
                data = await response.json()
                return web.json_response(data)
    else:
        return web.Response(text="Access token not found")

async def main() -> None:
    app = web.Application()
    app.router.add_get('/spotify/login', login)
    app.router.add_get('/spotify/callback', callback)
    app.router.add_get('/spotify/tracks', get_user_tracks)

    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, 'localhost', 8080)
    await site.start()

    while True:
        await asyncio.sleep(3600)  # Sleep for an hour or any desired interval

if __name__ == "__main__":
    asyncio.run(main())
