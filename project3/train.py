'''Created by nomanshafqat at 2020-04-02'''
import csv

import joblib

from UCT import UCT
from config import config
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.neural_network import MLPClassifier

import numpy as np
from play_game import UCTPlayGame


def concat_all_datasets(csv_logs_path, i):
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

        # break
    return whole_data


target_dir = config["target_dir"]
classifier = None

for i in range(0,config["total_iterations"]):
    print("iteration = ", i)
    config["legal"]=1
    config["illegal"]=1


    csv_logs_path = os.path.join(target_dir, "game_logs")
    model_logs_path = os.path.join(target_dir, "models")

    csvPath = os.path.join(csv_logs_path, "OthelloState_log" + str(i) + ".csv")
    modelPath = os.path.join(model_logs_path, "OthelloState_model" + str(i) + ".pkl")

    modelPath_last = os.path.join(model_logs_path, "OthelloState_model" + str(i-1) + ".pkl")

    if not os.path.exists(csv_logs_path):
        os.mkdir(csv_logs_path)
    if not os.path.exists(model_logs_path):
        os.mkdir(model_logs_path)

    writer = csv.writer(open(csvPath, 'w', newline='\n'))

    if i==0:
        classifier=None
    else:
        classifier = joblib.load(modelPath_last)


    num_of_games = 1000
    wins = []
    for j in range(num_of_games):
        wins.append(UCTPlayGame(classifier=classifier,classifier2=classifier,writer=writer))
        # print(wins)
        print(j,"/", num_of_games, " win % = ", wins.count("expert") / len(wins), "loss % = ",wins.count("apprentice")/len(wins), " draw % = ",(len(wins)-wins.count("apprentice")-wins.count("expert")) /len(wins))

    dataset = concat_all_datasets(csv_logs_path, i)
    Y = dataset.iloc[:, -1]
    X = np.array(dataset)[:, :-1]
    # print(X.shape,Y.shape)

    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.2, stratify=Y)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)

    clf2 = MLPClassifier()
    clf2 = clf2.fit(X_train, y_train)


    joblib.dump(clf,modelPath)
    print(clf.score(X_test, y_test), len(Y))
    print("clf2 ", clf2.score(X_test, y_test), len(Y))


    # print()
    # print(np.concatenate([np.expand_dims(clf.predict(X_test),axis=-1), np.expand_dims(np.array(y_test),axis=-1)],axis=-1))
