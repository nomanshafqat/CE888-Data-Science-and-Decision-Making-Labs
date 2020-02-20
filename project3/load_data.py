'''Created by nomanshafqat at 2020-02-20'''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.neural_network import MLPClassifier

import numpy as np

dataset=pd.read_csv('8_OthelloState.csv',header=None)
Y=dataset[65]
X = np.array(dataset)[:,:-1]


X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.33, stratify=Y)
clf = tree.DecisionTreeClassifier()
# clf = MLPClassifier(verbose=True)
clf = clf.fit(X_train, y_train)
print(clf.score(X_test,y_test),len(Y))

print(clf.predict(X_test) ,np.array(y_test))
