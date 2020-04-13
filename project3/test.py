'''Created by nomanshafqat at 2020-04-03'''
import csv
import os
import joblib
from config import config
from play_test_game import UCTPlayGame

target_dir = config["target_dir"]
classifier = None
import numpy as np
csv_logs_path = os.path.join(target_dir, "game_logs")
model_logs_path = os.path.join(target_dir, "models")
results_logs_path = os.path.join(target_dir, "results")

if not os.path.exists(csv_logs_path):
    os.mkdir(csv_logs_path)
if not os.path.exists(model_logs_path):
    os.mkdir(model_logs_path)

if not os.path.exists(results_logs_path):
    os.mkdir(results_logs_path)

win_rate=np.zeros((16,16))

for i in range(0,10,8):
    for j in range(0,i,1):

        print("iteration = ", i, j)
        config["legal"]=1
        config["illegal"]=1

        results_path= os.path.join(results_logs_path, "Othelloresukls_log" + str(i) +"_"+str(j)+".csv")

        print(results_path)
        modelPath_first = os.path.join(model_logs_path, "OthelloState_model" + str(i) + ".pkl")
        modelPath_second = os.path.join(model_logs_path, "OthelloState_model" + str(j) + ".pkl")

        writer = csv.writer(open(results_path, 'w', newline='\n'))


        if not os.path.exists(csv_logs_path):
            os.mkdir(csv_logs_path)
        if not os.path.exists(model_logs_path):
            os.mkdir(model_logs_path)

        expert_clf=joblib.load(modelPath_first)
        clf=joblib.load(modelPath_second)


        num_of_games = 10
        wins = []
        for k in range(num_of_games):
            wins.append(UCTPlayGame(classifier=clf, expert_clf=expert_clf, writer=None))
            print(wins)
            print("percentage = ",(wins.count("expert")+wins.count(0))/len(wins))


        writer.writerow(["percentage = ",(wins.count("expert")+wins.count(0))/len(wins)])
        win_rate[i][j]=wins.count("expert")/len(wins)

        np.save("1-30-5.npy", win_rate)

        # print()
        # print(np.concatenate([np.expand_dims(clf.predict(X_test),axis=-1), np.expand_dims(np.array(y_test),axis=-1)],axis=-1))
