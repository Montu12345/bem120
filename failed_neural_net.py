import tensorflow as tf
from tensorflow.keras import datasets
from keras.layers import Dense, Dropout, Flatten
from keras.models import Model, Sequential
from sklearn.model_selection import train_test_split
from scipy.spatial import distance
import numpy as np
import pandas as pd
import sys
from sklearn.inspection import permutation_importance
from keras import backend as K

# calcuating distance
def calculate_distance(player_coords):
    dist = tf.constant(0.0)
    for i in range(len(player_coords)):
        j = i
        while j < len(player_coords):
            a = tf.cast(player_coords[i], dtype=tf.float32)
            b = tf.cast(player_coords[j], dtype=tf.float32)
            dist += tf.subtract(a, b) 
            j += 1
    return dist

# calculating softmax
def softmax(vector):
    vector = [tf.cast(vector, dtype=tf.float32) for tensor in vector]
    return tf.nn.softmax(vector)

# reading in data
data = pd.read_csv("data_with_defense.csv")
mappings = pd.read_csv("play_by_play.csv")

# finding players per lineup
players = []
lineups = pd.read_csv("lineups_with_codes.csv")
plus_minus = []
for i in range(len(lineups['Player_Codes'])):
    player_codes = lineups.iloc[i]['Player_Codes']
    player_plus_minus = lineups.iloc[i]['+/-']
    plus_minus.append(float(player_plus_minus))
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
            current_players.append(list((mappings.loc[mappings['ID'] == int(code)])['Player'])[0])
        players.append(current_players)

# defining custom loss function
class Custom_CE_Loss(tf.keras.losses.Loss):
    def __init__(self):
        super().__init__()
    def call(self, y_true, y_pred):
      
      distances = []
      for i in range(len(players)):
          lineup = players[i]
          player_list = []
          go = True
          for player in lineup:
              if len((data.index[data["Player"] == player].tolist())) > 0:
                  player_list.append(y_pred[data.index[data["Player"] == player].tolist()])
              else:
                  go = False
          if go:
              dist = calculate_distance(player_list)
              distances.append(tf.keras.losses.MeanAbsoluteError()(dist / 10000, plus_minus[i]))
      loss =  tf.reduce_mean(distances)
      return loss

# defining model
model=Sequential()
model.add(Dense(45, activation='sigmoid', input_shape = (45,)))
# model.add(tf.keras.layers.BatchNormalization(synchronized=True))
# model.add(Dense(16, activation='relu'))
# model.add(Dense(3, activation='sigmoid'))
model.summary()

# defining testing data
train_data = pd.read_csv("train.csv")
train_x = train_data.loc[:, train_data.columns != "Score"].values

# compiling and running model
model.compile(optimizer='adam',
              loss=Custom_CE_Loss(),
              metrics=['accuracy'])
K.set_value(model.optimizer.learning_rate, 0.001)
history = model.fit(x=train_data, y= tf.random.uniform(shape=[456, 45]), batch_size = 456,steps_per_epoch=1,  epochs=30)
for layer in model.layers: print(layer.get_weights())