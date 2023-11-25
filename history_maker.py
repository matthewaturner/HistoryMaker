"""
HistoryMaker.py

Usage:
    HistoryMaker.py create playlist --start=<start_date> --end=<end_date> --source=<source>

Options:
    -h --help       Show this help message and exit.

Commands:
    create playlist    Create a playlist based on historical data.

Arguments:
    --start=<start_date>    Start date for the playlist in the format yyyy-mm-dd.
    --end=<end_date>        End date for the playlist in the format yyyy-mm-dd.
    --source=<source>       Source for historical data.

Examples:
    HistoryMaker.py create playlist --start=2023-01-01 --end=2023-01-31 --source=spotify
"""

if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)
    print(arguments)
