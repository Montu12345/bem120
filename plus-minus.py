# imports
import pandas as pd 
import numpy as np

# calculating average +/- scores across all seasons
player_data = pd.read_csv('player_data.csv')
original_stats = pd.read_csv('original_stats.csv')
avg_scores = []
for name in original_stats["Player"]:
    stats = player_data.loc[player_data["Player"] == name]
    if len(stats) > 1:
        score = 0
        for plus_minus in stats["plus_minus_score"]: 
            score += float(plus_minus)
        score = score / len(stats["plus_minus_score"])
        avg_scores.append(score)
    else:
        avg_scores.append(None)

# adding plus minus scores to dataframe
original_stats["plus_miuns_scores"] = avg_scores

# assigning players classes based on plus minus scores
class_score = []
for score in avg_scores:
    if score == None:
        class_score.append(None)
        continue
    if score < 0.75:
        class_score.append(0)
    else:
        class_score.append(1)

# saving class
original_stats["class_plus_miuns_scores"] = class_score

# dropping null values
original_stats = original_stats.dropna()