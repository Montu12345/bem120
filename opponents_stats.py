import pandas as pd 
import numpy as np

# parsing through opponents stats and putting into dataframe

files = ['2010-11.csv', '2011-12.csv', '2012-13.csv', '2013-14.csv', 
         '2014-15.csv', '2015-16.csv', '2016-17.csv', '2017-18.csv', 
         '2019-20.csv', '2020-21.csv', '2021-22.csv']
opp_stats = pd.DataFrame()
for i in files:
    opp_stats = pd.concat([opp_stats, pd.read_csv(f'opponent_stats/{i}')])

opp_stats_vals = []

for row in opp_stats['\tRESTRICTED AREA\tIN THE PAINT']:
    if "-" not in row:
        opp_stats_vals.append(row.split("\t"))
        
opp_stats_clean = pd.DataFrame()
for i in range(1, len(opp_stats_vals)):
    if len(opp_stats_vals[i]) == 24:
        opp_stats_clean["a" + str(i)] = opp_stats_vals[i]

opp_stats_clean = opp_stats_clean.T
opp_stats_clean.dropna()

# fixing column names
opp_stats_clean = opp_stats_clean.rename(columns={0: "Player", 1: "Team", 
                                                  2: "age", 
                                                  3:"restricted_area_fgm", 
                                                  4: "restricted_area_fga", 
                                                  5: "restricted_area_fgp", 
                                                  6: "in_paint_fgm", 
                                                  7: "in_paint_fga", 
                                                  8: "in_paint_fgp", 
                                                  9: "mid_range_fgm", 
                                                  10: "mid_range_fga", 
                                                  11: "mid_range_fgp", 
                                                  12: "left_corner3_fgm", 
                                                  13: "left_corner3_fga", 
                                                  14: "left_corner3_fgp", 
                                                  15: "right_corner3_fgm", 
                                                  16: "right_corner3_fga", 
                                                  17: "right_corner3_fgp", 
                                                  18: "corner3_fgm", 
                                                  19: "corner3_fga", 
                                                  20: "corner3_fgp", 
                                                  21: "above_break3_fgm", 
                                                  22: "above_break3_fga", 
                                                  23:"above_break3_fgp "})

# converting statistics from strings to floats
original_stats = pd.read_csv('original_stats')
restricted_area_fgm = []
restricted_area_fga = []
restricted_area_fgp = []

in_paint_fgm = []
in_paint_fga = []
in_paint_fgp = []

mid_range_fgm = []
mid_range_fga = []
mid_range_fgp = []

left_corner3_fgm = []
left_corner3_fga = []
left_corner3_fgp = []

right_corner3_fgm = []
right_corner3_fga = []
right_corner3_fgp = []

corner3_fgm = []
corner3_fga = []
corner3_fgp = []

above_break3_fgm = []
above_break3_fga = []
above_break3_fgp = []

for name in original_stats["Player"]:
    stats = opp_stats_clean.loc[opp_stats_clean["Player"] == name]
    print(stats)
    restricted_area_fgm.append(np.mean([float(value) for value in list(stats['restricted_area_fgm'])]))
    restricted_area_fga.append(np.mean([float(value) for value in list(stats['restricted_area_fga'])]))
    restricted_area_fgp.append(np.mean([float(value) for value in list(stats['restricted_area_fgp'])]))

    in_paint_fgm.append(np.mean([float(value) for value in list(stats['in_paint_fgm'])]))
    in_paint_fga.append(np.mean([float(value) for value in list(stats['in_paint_fga'])]))
    in_paint_fgp.append(np.mean([float(value) for value in list(stats['in_paint_fgp'])]))

    mid_range_fgm.append(np.mean([float(value) for value in list(stats['mid_range_fgm'])]))
    mid_range_fga.append(np.mean([float(value) for value in list(stats['mid_range_fga'])]))
    mid_range_fgp.append(np.mean([float(value) for value in list(stats['mid_range_fgp'])]))

    left_corner3_fgm.append(np.mean([float(value) for value in list(stats['left_corner3_fgm'])]))
    left_corner3_fga.append(np.mean([float(value) for value in list(stats['left_corner3_fga'])]))
    left_corner3_fgp.append(np.mean([float(value) for value in list(stats['left_corner3_fgp'])]))

    right_corner3_fgm.append(np.mean([float(value) for value in list(stats['right_corner3_fgm'])]))
    right_corner3_fga.append(np.mean([float(value) for value in list(stats['right_corner3_fga'])]))
    right_corner3_fgp.append(np.mean([float(value) for value in list(stats['right_corner3_fgp'])]))

    corner3_fgm.append(np.mean([float(value) for value in list(stats['corner3_fgm'])]))
    corner3_fga.append(np.mean([float(value) for value in list(stats['corner3_fga'])]))
    corner3_fgp.append(np.mean([float(value) for value in list(stats['corner3_fgp'])]))

    above_break3_fgm.append(np.mean([float(value) for value in list(stats['above_break3_fgm'])]))
    above_break3_fga.append(np.mean([float(value) for value in list(stats['above_break3_fga'])]))
    above_break3_fgp.append(np.mean([float(value) for value in list(stats['above_break3_fgp '])]))
    
original_stats["restricted_area_fgm"] = restricted_area_fgm
original_stats["restricted_area_fga"] = restricted_area_fga
original_stats["restricted_area_fgp"] = restricted_area_fgp

original_stats["in_paint_fgm"] = in_paint_fgm
original_stats["in_paint_fga"] = in_paint_fga
original_stats["in_paint_fgp"] = in_paint_fgp

original_stats["mid_range_fgm"] = mid_range_fgm
original_stats["mid_range_fga"] = mid_range_fga
original_stats["mid_range_fgp"] = mid_range_fgp

original_stats["left_corner3_fgm"] = left_corner3_fgm
original_stats["left_corner3_fga"] = left_corner3_fga
original_stats["left_corner3_fgp"] = left_corner3_fgp

original_stats["right_corner3_fgm"] = right_corner3_fgm
original_stats["right_corner3_fga"] = right_corner3_fga
original_stats["right_corner3_fgp"] = right_corner3_fgp

original_stats["corner3_fgm"] = corner3_fgm
original_stats["corner3_fga"] = corner3_fga
original_stats["corner3_fgp"] = corner3_fgp

original_stats["above_break3_fgm"] = above_break3_fgm
original_stats["above_break3_fga"] = above_break3_fga
original_stats["above_break3_fgp"] = above_break3_fgp

original_stats.to_csv("data_with_defense.csv")