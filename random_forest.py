# code for feature importance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# read in data
t = pd.read_csv("data_with_defense copy 3.csv")

depth = []
error = []
dict_scores = {}

# normalizing values
for col in t.columns:
  if col == "class_plus_miuns_scores":
    continue
  t[col] = t[col] / max(t[col])

# defining testing and training data
X = (t.loc[:400, t.columns != "class_plus_miuns_scores"].values)
y = (t.loc[:400, t.columns == "class_plus_miuns_scores"].values)
X_test = (t.loc[400:, t.columns != "class_plus_miuns_scores"].values)
y_test = (t.loc[400:, t.columns == "class_plus_miuns_scores"].values)

# creating model for max_depth = 1-9 and calculating feature importance
for i in range(1, 10):
    clf = RandomForestClassifier(max_depth=i, random_state=0)
    model = clf.fit(X, y.ravel())
    predictions = clf.predict(X_test)

    wrong = 0
    for pred in range(len(predictions)):
        if (predictions[pred] != y_test.ravel()[pred]):
            wrong += 1
    depth.append(i)
    error.append(wrong / len(predictions))
    print()
    print(wrong / len(predictions))
    r = permutation_importance(model, X, y,
                                n_repeats=30,
                                random_state=0, scoring='r2')
    j = len(r.importances_mean.argsort())
    for idx in r.importances_mean.argsort()[::-1]:
            # if r.importances_mean[idx] - 2 * r.importances_std[idx] > 0:
            if str(t.columns[idx]) not in dict_scores:
                dict_scores[str(t.columns[idx])] = r.importances_mean[idx]# j
            else:
                dict_scores[str(t.columns[idx])] += r.importances_mean[idx]# j
            j -= 1
            print(f"{t.columns[idx] :<8}"
                f"{r.importances_mean[idx]:.3f}"
                f" +/- {r.importances_std[idx]:.3f}")

# printing out final results
sorted(dict_scores.items())

# plotting model error vs max_depth
plt.plot(depth, error)
plt.xlabel("max_depth")
plt.ylabel("error")