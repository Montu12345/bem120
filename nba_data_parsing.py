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

# splitting opponents stats
opponents_stats_df = pd.read_csv('opponents_stats.csv')
opponent_stats = []
for i in opponents_stats_df['RESTRICTED AREA\tIN THE PAINT']:
    opponent_stats.append(i.replace("-", "N/A").split("\t"))
    
# splitting box stats 
box_score_stats_df = pd.read_csv("box_score_stats.csv")
box_score_stats = []
for i in box_score_stats_df['#\tPLAYER\tGP\tMIN\tPTS\tFGM\tFGA\tFG%\t3PM\t3PA\t3P%\tFTM\tFTA\tFT%\tOREB\tDREB\tREB\tAST\tSTL\tBLK\tTOV\tEFG%\tTS%']:
    box_score_stats.append(i.replace("-", "N/A").split("\t"))