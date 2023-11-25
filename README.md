# HistoryMaker
An app that I can run periodically to organize my music into playlists by month.

## Documentation Links
 - [Spotify Web API](https://developer.spotify.com/documentation/web-api)
 - [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
 - [Spotify PyPi SDK](https://pypi.org/project/spotify/)

## Plan

### Option 1
Using python3, define a command line tool with the following commands:

"""History Maker.

Usage:
  history_maker.py new playlist <name> --start=<start> --end=<end>

Options:
  --start=<start>    The start date, inclusive. ISO-8601 format.
  --end=<end>        The end date, exclusive. ISO-8601 format.
  --confirm          Allows user to confirm y/n before creating playlist.
"""

### Option 2
Lightweight flask app that runs a local website (flask app) with a very simple form-based UI.

Pros:
 - Hostable once you're done
 
