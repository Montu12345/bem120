# finds the codes of the players in the lineups

# imports
from sklearn.cluster import KMeans
from sklearn import preprocessing
import sklearn.cluster as cluster
import sklearn.metrics as metrics
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
from matplotlib import pyplot as plt
# %matplotlib inline
import os
import numpy as np

# loading in data
player_basic_stats_df = pd.read_csv('player_basic_stats.csv')
mappings = pd.read_csv("play_by_play_data.csv")

# get codes for player given first initial, last namem, and season
def get_code(player, season):
    q = player_basic_stats_df.loc[player_basic_stats_df['season'] == season]
    for i in range(len(q)):
        list_ver = list(q.iloc[i])
        list_name = list_ver[1].split(" ")
        if len(list_name) < 2:
            last_name = list_name[0]
            first_initial = list_name[0]
            if first_initial == player:
                player_stats = list((mappings.loc[mappings['Player'] == first_initial])['ID']) 
                if len(player_stats) > 0:
                    return player_stats[0]
                else:
                    return "N/A"
        else:
            first_initial = list_name[0][0] + "."
            last_name = list_name[1]
            if (first_initial + " " + last_name) == player:
                player_stats = list((mappings.loc[mappings['Player'] == (list_name[0] + " " + last_name)])['ID'])
                if (len(player_stats) > 0):
                    return player_stats[0]
                else:
                    return "N/A"
    return "N/A"

# find codes for each set of players
def find_player_codes(list_player_names, season):
    codes = []
    for player in list_player_names:
        codes.append(get_code(player, season))
    return codes

# extract players per lineup
lineups_data_df = pd.read_csv('lineups_data.csv')
all_codes = []
for val in range(len(lineups_data_df)):
    list_ver = list(lineups_data_df.iloc[val])
    season = list_ver[1]
    players = list_ver[2].split(" - ")
    all_codes.append(find_player_codes(players, season))
    
    
# convert lineup codes to integers (they were saved as integers)
# only find player names for lineups with all valid players (no "N/A")
players = []
lineups = pd.read_csv("lineups_with_codes.csv")
for player_codes in lineups['Player_Codes']:
    player_codes = player_codes.replace("[", "")
    player_codes = player_codes.replace("]", "")
    player_codes = player_codes.split(",")
    current_players = []
    go = True
    for code in player_codes:
        if code == " 'N/A'" or code == "'N/A'":
            go = False
            continue
    if go:
        for code in player_codes:
            current_players.append(list((mappings.loc[mappings['PLAYER_ID'] == int(code)])['PLAYER_NAME'])[0])
    players.append(current_players)
    
# calculating distance between each player's vector
def calculate_distance(player_list):
    distance = 0
    for i in range(len(player_list)):
        j = i
        while j < len(player_list):
            distance += np.linalg.norm(player_list[i] - player_list[j])
            j += 1
    return distance

# iterating through lineup data and calculating distances
data = pd.read_csv("data_with_defense_stats.csv")
distances = []
for lineup in players:
    player_list = []
    go = True
    for player in lineup:
        if len((data.loc[data["Player"] == player].values)) > 0:
            player_list.append(data.loc[data["Player"] == player].values)
        else:
            go = False
    if go:
        for i in range(len(player_list)):
            for j in range(len(player_list[i])):
                for k in range(len(player_list[i][j])):
                    if type(player_list[i][j][k]) == str:
                        player_list[i][j][k] = 0
        distances.append(calculate_distance(player_list))
    else:
        distances.append("None")
