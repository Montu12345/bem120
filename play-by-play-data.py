# collects play by play data, only shots though

# imports
from py_ball import league, player
import pandas as pd
from time import sleep

# headers + season

HEADERS = {'Connection': 'keep-alive',
           'Host': 'stats.nba.com',
           'Origin': 'http://stats.nba.com',
           'Upgrade-Insecure-Requests': '1',
           'Referer': 'stats.nba.com',
           'x-nba-stats-origin': 'stats',
           'x-nba-stats-token': 'true',
           'Accept-Language': 'en-US,en;q=0.9',
           "X-NewRelic-ID": "VQECWF5UChAHUlNTBwgBVw==",
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
               AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
year = '2010-11' # adjust year as needed

# collecting all of the game ids

shot_details = pd.DataFrame()

schedule = league.League(headers=HEADERS, endpoint='leaguegamelog', season=year).data
game_info = schedule['LeagueGameLog']
game_ids = []

for i in range(len(game_info)):
    game_ids.append(game_info[i]['GAME_ID'])
game_ids = set(game_ids)

# collecting every shot per game

for game in game_ids:
    print(game)
    league_id = '00'
    player_id = '0'
    game_id = str(game)
    season = year
    shots = player.Player(headers=HEADERS,
                          endpoint='shotchartdetail',
                          league_id=league_id,
                          player_id=player_id,
                          game_id=game_id,
                          season=season)
    shot_df = pd.DataFrame(shots.data['Shot_Chart_Detail'])
    shot_details = pd.concat([shot_df, shot_details])
    sleep(3)
