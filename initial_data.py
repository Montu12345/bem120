# initial data combination and analysis

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
from sklearn.decomposition import PCA

# reading in assists and height data
files = ['assists_info/assists-2010-11.csv', 'assists_info/assists-2011-12.csv', 'assists_info/assists-2012-13.csv', 'assists_info/assists-2013-14.csv', 'assists_info/assists-2014-15.csv', 'assists_info/assists-2015-16.csv', 'assists_info/assists-2017-18.csv', 'assists_info/assists-2018-19.csv', 'assists_info/assists-2019-20.csv', 'assists_info/assists-2020-21.csv', 'assists_info/assists-2021-22.csv', 'assists_info/assists-2022-23.csv']
def load_data(files):
    df_all_data = pd.DataFrame()
    for file in files:
        new_file = pd.read_csv(file)
        df_all_data = pd.concat([new_file, df_all_data])
    return df_all_data
assists_df = load_data(files)
heights_df = pd.read_csv('all_seasons.csv')

# Player Code, MEAN X, MEAN Y, STD X, STD Y, VAR X, VAR Y, Player Pos, 
# Assists% Avg, Minutes Played, Avg, Height, PPG calculations per player
# exclude players that have same names
all_data = pd.DataFrame()
unknowns = ["Chris Johnson", "Mike James", "Chris Wright"]
column_names = ['Player Code', 'MEAN X', 'MEAN Y', 'STD X', 'STD Y', 
                'VAR X', 'VAR Y', 'Player Pos', "Assists% Avg", 
                "Minutes Played Avg", "Height", "PPG"]
for file in os.listdir("./player_stats"):
        filename = os.fsdecode(file)
        if filename == '.DS_Store':
            continue
        df_player_stats = pd.read_csv(f'./player_stats/{filename}')
        x_loc = df_player_stats['LOC_X']
        y_loc = df_player_stats['LOC_Y']
        player_name = list(df_player_stats['PLAYER_NAME'])[0]
        one = assists_df.loc[assists_df['Player'] == player_name]['AST%']
        two = assists_df.loc[assists_df['Player'] == player_name]['MP']
        if len(list((a.loc[a['PLAYER_NAME'] == player_name])['Positions'])) < 1:
            player_pos = None
        else:
            player_pos = list((a.loc[a['PLAYER_NAME'] == player_name])['Positions'])[0]
        if len(list(one)) < 1:
            assists_avg = None
        else:
            assists_avg = np.mean(list(one))
        if len(list(two)) < 1:
            minutes_played_avg = None
        else:
            minutes_played_avg = np.mean(list(two))
        if len(list(heights_df.loc[heights_df['player_name'] == player_name]['player_height'])) < 1:
            height = None
        else:
            height = list((heights_df.loc[heights_df['player_name'] == player_name])['player_height'])[0]
        if len(list(heights_df.loc[heights_df['player_name'] == player_name]['pts'])) < 1:
            points = None
        else:
            points = np.mean(list((heights_df.loc[heights_df['player_name'] == player_name])['pts']))
        unknowns = ["Chris Johnson", "Mike James", "Chris Wright"]
        player_id = df_player_stats['PLAYER_ID'][0]
        shot_locations = np.zeros((len(x_loc), 2))
        for i in range(len(x_loc)):
            shot_locations[i] = [x_loc[i], y_loc[i]]
        mean = shot_locations.mean(axis= 0)
        std = shot_locations.std(axis= 0)
        var = shot_locations.var(axis= 0)
        new_data = [player_id, mean[0], mean[1], std[0], std[1], var[0], var[1], player_pos, assists_avg, minutes_played_avg, height, points]
        new_pd = pd.DataFrame([new_data], columns=column_names)
        all_data = pd.concat([all_data, new_pd], axis=0)
        
# saving data to file
all_data.drop(columns='Unnamed: 0')
all_data.to_csv("number_value_data.csv")

# MEAN X, MEAN Y, STD X, STD Y, VAR X, VAR Y normalizing and saving to dataframe
scaler = MinMaxScaler()
scale = scaler.fit_transform(all_data[['MEAN X','MEAN Y', 'STD X', 'STD Y', 'VAR X', 'VAR Y']])
df_scale = pd.DataFrame(scale, columns = ['MEAN X','MEAN Y', 'STD X', 'STD Y', 'VAR X', 'VAR Y']);

# PCA dimentionality reduction
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(df_scale[['VAR X', 'VAR Y']])
pca_df = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])
pca_df.head()

# seeing optimal number of clusters
K=range(2,12)
wss = []
for k in K:
    kmeans=cluster.KMeans(n_clusters=k)
    kmeans=kmeans.fit(pca_df)
    wss_iter = kmeans.inertia_
    wss.append(wss_iter)
plt.xlabel('K')
plt.ylabel('Within-Cluster-Sum of Squared Errors (WSS)')
plt.plot(K,wss)

# scaling assists and ppg by minutes played
all_data['Scaled Assists'] = all_data['Assists% Avg'] / all_data['Minutes Played Avg'] * 1000
all_data['Scaled PPG'] = all_data['PPG'] / all_data['Minutes Played Avg'] * 1000

# plot
sns.scatterplot(x="Player Pos", y="Assists% Avg",hue = 'STD X',  
                data=all_data.loc[((all_data['Height'] > 0) & 
                                  (all_data['Scaled Assists'] < 20) & 
                                  (all_data['Scaled PPG'] < 12))],
                palette='viridis')

# Kmeans clustering functions
def cluster_graph(dataframe):
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(dataframe)
    pca_df = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
    pca_df.head()
    weight = pca.components_
    print(weight)
    K=range(2,30)
    wss = []
    for k in K:
        kmeans=cluster.KMeans(n_clusters=k)
        kmeans=kmeans.fit(pca_df)
        wss_iter = kmeans.inertia_
        wss.append(wss_iter)
    plt.xlabel('K')
    plt.ylabel('Within-Cluster-Sum of Squared Errors (WSS)')
    plt.plot(K,wss)
    return pca_df

def create_clusters(dataframe, num_clusters):
    kmeans = cluster.KMeans(n_clusters=num_clusters)
    kmeans = kmeans.fit(dataframe)
    dataframe['Clusters'] = kmeans.labels_
    sns.scatterplot(x="principal component 1", y="principal component 2",hue = 'Clusters',  data=dataframe,palette='viridis')
    return dataframe