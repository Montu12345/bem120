# combines all the play by play data from each season and creates heatmaps
# for each player

# imports
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

# loading in all play by play data

def load_data(files):
    df_all_data = pd.DataFrame()
    for file in files:
        new_file = pd.read_csv(f'shot_info/{file}')
        df_all_data = pd.concat([new_file, df_all_data])
    return df_all_data

# files containing play by play data
files = ['shot_details_2010-11.csv', 
         'shot_details_2011-12.csv', 
         'shot_details_2012-13.csv', 
         'shot_details_2012-13.csv', 
         'shot_details_2019-20.csv', 
         'shot_details_2019-20.csv', 
         'shot_details_2019-20.csv', 
         'shot_details_2020-21.csv', 
         'shot_details_2021-22.csv', 
         'shot_details_2022-23.csv']

df_all_data = load_data(files)

# unique player ids
print(len(set(df_all_data['PLAYER_ID'])))

# getting all unique player ids
player_stats_dict = {}

for player in set(df_all_data['PLAYER_ID']):
    player_stats_dict[str(player)] = []
    
# condensing all data into one dataframe using player id
for value in player_stats_dict:
    player_stats_dict[value] = df_all_data[df_all_data['PLAYER_ID'] == int(value)]
    
# creating separate folder for each player_id
for value in player_stats_dict:
    os.mkdir(f'player_info/{value}')
    player_stats_dict[value].to_csv(f'player_info/{value}/stats.csv')

# Function to draw basketball court and save image
def create_court(ax, color, num, name):
    # Short corner 3PT lines
    ax.hexbin(player_stats_dict[num]['LOC_X'], player_stats_dict[num]['LOC_Y'] + 60, gridsize=(30, 30), extent=(-300, 300, 0, 940), bins='log', cmap='Blues')
    ax.text(0, 1.05, name, transform=ax.transAxes, ha='left', va='baseline')
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))
    # Rim
    ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))

    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
    # Remove ticks
#     ax.set_xticks([])
#     ax.set_yticks([])

    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    plt.savefig(f'player_info/{num}/heat_map.png', bbox_inches='tight')

# create heat map for each player
for value in player_stats_dict:
    # General plot parameters
    mpl.rcParams['font.family'] = 'Avenir'
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.linewidth'] = 2
    # Draw basketball court
    fig = plt.figure(figsize=(4, 3.76))
    ax = fig.add_axes([0, 0, 1, 1])
    name = list(player_stats_dict[value]['PLAYER_NAME'])[0]
    ax = create_court(ax, 'black', value, name)