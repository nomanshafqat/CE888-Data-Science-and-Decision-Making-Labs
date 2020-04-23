'''Created by nomanshafqat at 2020-04-02'''
import csv
import threading
import joblib
from config import config
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.neural_network import MLPClassifier

from playGame import UCTPlayGame
from concatDatasets import concatAllDatasets

target_dir = config["target_dir"]
classifier = None

# main loop runs from 0 to n iterations
for i in range(0, config["total_iterations"]):
    print("iteration = ", i)
    # numbers that track legal and illegal moves
    config["legal"] = 1
    config["illegal"] = 1

    # path for game logs
    csv_logs_path = os.path.join(target_dir, "game_logs")
    # path for models
    model_logs_path = os.path.join(target_dir, "models")

    # csv path for writing
    csvPathWriting = os.path.join(csv_logs_path, "OthelloState_log" + str(i) + ".csv")
    modelPath = os.path.join(model_logs_path, "OthelloState_model" + str(i) + ".pkl")
    modelPath_last = os.path.join(model_logs_path, "OthelloState_model" + str(i - 1) + ".pkl")

    if not os.path.exists(csv_logs_path):
        os.mkdir(csv_logs_path)
    if not os.path.exists(model_logs_path):
        os.mkdir(model_logs_path)
    writer = csv.writer(open(csvPathWriting, 'w', newline='\n'))

    # for first iteration there is no model else load the model of previous iteration
    if i == 0:
        classifier = None
    else:
        classifier = joblib.load(modelPath_last)

    # play 50 games in batches of 5 threads
    num_of_games = 50
    number_of_threads = 5
    wins = []
    lock = threading.Lock()

    for alpha in range(0, num_of_games, number_of_threads):
        threads = []
        thred_wins = []
        game_logs = []
        # Define and start threds
        for j in range(number_of_threads):
            threads.append(
                threading.Thread(target=UCTPlayGame, name=str(i), args=(classifier, classifier, thred_wins, game_logs)))
            threads[j].start()
        #join threads
        for j in range(number_of_threads):
            threads[j].join()

        #write the logs
        for j in range(number_of_threads):
            writer.writerows(game_logs[j])
        wins = wins + thred_wins

        #print progress
        print(alpha + number_of_threads, "/", num_of_games, " win % = ", wins.count("expert") / len(wins), "loss % = ",
              wins.count("apprentice") / len(wins), " draw % = ",
              (len(wins) - wins.count("apprentice") - wins.count("expert")) / len(wins))

    # Train a DT and MLP model and compares and only save DT model.
    dataset = concatAllDatasets(csv_logs_path, i)
    Y = dataset.iloc[:, -1]
    X = np.array(dataset)[:, :-1]

    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.2, stratify=Y)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)

    clf2 = MLPClassifier()
    clf2 = clf2.fit(X_train, y_train)

    joblib.dump(clf, modelPath)
    print("DT ", clf.score(X_test, y_test), len(Y))
    print("MLP ", clf2.score(X_test, y_test), len(Y))
