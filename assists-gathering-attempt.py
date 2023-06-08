# failed attempt at attempting to get assists data from NBA website

# imports
from itertools import chain
from pathlib import Path
from time import sleep
from datetime import datetime
import requests
from tqdm import tqdm
import numpy as np
import pandas as pd

tqdm.monitor_interval = 0

PROJECT_DIR = Path.cwd().parent 
DATA_DIR = PROJECT_DIR / 'data' / 'scraped' / 'teamgamelogs'
DATA_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_DIR = PROJECT_DIR / 'data' / 'prepared'
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' +
    'AppleWebKit/537.36 (KHTML, like Gecko) ' +
    'Chrome/61.0.3163.100 Safari/537.36'
)

REQUEST_HEADERS = {
    'user-agent': USER_AGENT,
}

NBA_URL = 'http://stats.nba.com/stats/teamgamelogs'
NBA_ID = '00'

NBA_SEASON_TYPES = {
    'regular': 'Regular Season',
    'playoffs': 'Playoffs',
    'preseason': 'Pre Season',
}

season = '2016-17'
season_type = NBA_SEASON_TYPES['regular']

nba_params = {
    'LeagueID': NBA_ID,
    'Season': season,
    'SeasonType': season_type,
}

r = requests.get(NBA_URL, params=nba_params, headers=REQUEST_HEADERS, allow_redirects=False)
r.status_code