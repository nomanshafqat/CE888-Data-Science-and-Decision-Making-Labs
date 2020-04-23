'''Created by nomanshafqat at 4/15/20'''
import os
import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from concatDatasets import concatAllDatasets
from config import config

target_dir = config["target_dir"]
classifier = None

csv_logs_path = os.path.join(target_dir, "game_logs")

# variables that store accuracy for each iteration
decision_tree_classifier = []
MLP_classifier = []
Random = []

break_ = False
for i in range(0, 20):
    # fetches the dataset
    dataset = concatAllDatasets(csv_logs_path, i, break_=break_)
    Y = dataset.iloc[:, -1]
    X = np.array(dataset)[:, :-1]
    # print(X.shape,Y.shape)

    # splits into train and test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.2, stratify=Y)

    # trains DT
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)

    # trains MLP
    clf2 = MLPClassifier()
    clf2 = clf2.fit(X_train, y_train)

    # calculates scores and appends into the list
    decision_tree_classifier.append(clf.score(X_test, y_test))
    MLP_classifier.append(clf2.score(X_test, y_test))
    Random.append(1 / 64)

    print(decision_tree_classifier[i], MLP_classifier[i], len(y_train))

# plots the results
import matplotlib.pyplot as plt

xaxis = [int(i) for i in range(1, 21)]
plt.figure(figsize=(15, 8))
plt.plot(decision_tree_classifier,
         label="Decision Tree ( mean = " + str(int(100 * np.mean(decision_tree_classifier)) / 100) + ")")
plt.hlines(np.mean(decision_tree_classifier), 0, 19)

plt.plot(MLP_classifier, label="Neural Network(MLP) ( mean = " + str(int(100 * np.mean(MLP_classifier)) / 100) + ")")
plt.hlines(np.mean(MLP_classifier), 0, 19)
plt.plot(Random, label="Random")
plt.legend(loc="lower left", fontsize=20)
plt.xlabel('Number of Iterations', fontsize=20)
plt.ylabel('Accuracy', fontsize=20)
plt.xticks(xaxis, xaxis)
plt.savefig(str(break_) + ".png")

plt.show()
