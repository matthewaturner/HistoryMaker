import asyncio
import json
import spotify
from spotify import Client
from aiohttp import web
from aiohttp.web import AppRunner, TCPSite
from contextvars import ContextVar

def load_config() -> json:
    with open('config.json', 'r') as f:
        return json.load(f)

config: json = load_config()
CLIENT_ID: str = config['spotify']['client_id']
CLIENT_SECRET: str = config['spotify']['client_secret']
REDIRECT_URI: str = 'http://localhost:8080/callback'

CLIENT: ContextVar[spotify.Client] = ContextVar("spotify_client")

async def callback(request):
    client = CLIENT.get()
    user = await spotify.User.from_code(
        client=client,
        code=request.query['code'],
        redirect_uri=REDIRECT_URI,
    )
    tracks = await user.library.get_all_tracks()
    return web.HTTPFound(repr(tracks))


async def main() -> None:
    async with spotify.Client(CLIENT_ID, CLIENT_SECRET) as client:
        CLIENT.set(client)
        app = web.Application()
        runner = AppRunner(app)
        await runner.setup()
        site = TCPSite(runner, 'localhost', 8080)
        await site.start()

        # Keep the event loop running
        while True:
            await asyncio.sleep(3600)  # Sleep for an hour or any desired interval

if __name__ == "__main__":
    asyncio.run(main())
