'''Created by nomanshafqat at 2020-02-20'''
import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.neural_network import MLPClassifier

import numpy as np


def concat_all_datasets(csv_logs_path="Logs3/game_logs", i=15):
    whole_data = None
    # print(str(type(whole_data)))
    for j in range(max(0,i-100), i + 1):
        csvPath = os.path.join(csv_logs_path, "OthelloState_log" + str(j) + ".csv")
        print(j, csvPath)

        dataset_ = pd.read_csv(csvPath, header=None,delimiter = ",")

        # print(dataset_.shape)
        if str(type(whole_data)) == "<class 'NoneType'>":
            # print("herej")
            whole_data = dataset_.copy()
        else:
            # whole_data = pd.concat([whole_data, dataset_], ignore_index=True)
            whole_data = whole_data.append(dataset_)
            # print(whole_data.shape, "cocat")

    return whole_data


dataset=concat_all_datasets()
print(dataset)
Y=dataset.iloc[:,-1]
print(Y)
X = np.array(dataset)[:,:-1]


X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.33,stratify=Y)

clf = MLPClassifier(verbose=False)
clf = clf.fit(X_train, y_train)
print(clf.score(X_test,y_test),len(Y))

clf = tree.DecisionTreeClassifier()

# print(clf.predict(X_test),"\n" ,np.array(y_test))
clf = clf.fit(X_train, y_train)
print(clf.score(X_test,y_test),len(Y))

