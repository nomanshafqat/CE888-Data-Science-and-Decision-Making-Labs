'''Created by nomanshafqat at 2020-04-03'''
import csv
import os
import joblib
from config import config
from play_game import UCTPlayGame

target_dir = config["target_dir"]
classifier = None

csv_logs_path = os.path.join(target_dir, "game_logs")
model_logs_path = os.path.join(target_dir, "models")
results_logs_path = os.path.join(target_dir, "results")

if not os.path.exists(csv_logs_path):
    os.mkdir(csv_logs_path)
if not os.path.exists(model_logs_path):
    os.mkdir(model_logs_path)

if not os.path.exists(results_logs_path):
    os.mkdir(results_logs_path)



for i in range(1,15,2):
    for j in reversed(range(0,i,2)):

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


        clf1=joblib.load(modelPath_first)
        clf2=joblib.load(modelPath_second)


        num_of_games = 10
        wins = []
        for j in range(num_of_games):
            wins.append(UCTPlayGame(classifier=clf1,classifier2=clf2,writer=None))
            print(wins)

        writer.writerow(wins)

        # print()
        # print(np.concatenate([np.expand_dims(clf.predict(X_test),axis=-1), np.expand_dims(np.array(y_test),axis=-1)],axis=-1))
