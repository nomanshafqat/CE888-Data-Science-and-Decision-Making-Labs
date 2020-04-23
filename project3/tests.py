import unittest
import matplotlib.pyplot as plt
import csv
import os
import joblib
from config import config
from playTestGame import UCTPlayTestGame

target_dir = config["target_dir"]
classifier = None
import numpy as np


class Unit_tests(unittest.TestCase):
    # the test data is visualised after testing in this function
    def test_visualisationResults(self):

        import numpy as np
        results = np.load("Logs/1-30-4.npy")
        # results = np.load("Logs6_6_1000_30games/1-30-5.npy")
        self.assertEqual(True, results is not None)

        for i in range(0, 21, 4):
            if i <= 7:
                continue
            print(results[i])

            xaxis = [int(j) for j in range(1, i)]
            plt.figure(figsize=(15, 8))
            print(results[i, :i])
            plt.plot(results[i][:i],
                     label=str(i) + "th Iteration ( mean = " + str(int(100 * np.mean(results[i][:i])) / 100) + ")")
            plt.hlines(np.mean(results[i][:i]), 0, i)

            plt.legend(loc="upper left", fontsize=20)
            plt.xlabel('Opponent of ' + str(i), fontsize=20)
            plt.ylabel('Winrate of ' + str(i) + "th iteration", fontsize=20)
            plt.ylim(0, 1)
            plt.xticks(xaxis, xaxis)
            plt.savefig(str(i) + "th.png")
            plt.show()

    # Iterations are evaluated using this functions
    def test_iterations(self):

        csv_logs_path = os.path.join(target_dir, "game_logs")
        model_logs_path = os.path.join(target_dir, "models")
        results_logs_path = os.path.join(target_dir, "results")

        if not os.path.exists(csv_logs_path):
            os.mkdir(csv_logs_path)
        if not os.path.exists(model_logs_path):
            os.mkdir(model_logs_path)

        if not os.path.exists(results_logs_path):
            os.mkdir(results_logs_path)

        win_rate = np.zeros((21, 21))

        for i in reversed(range(0, 21, 4)):
            for j in range(0, i, 1):

                print("iteration = ", i, j)
                config["legal"] = 1
                config["illegal"] = 1

                results_path = os.path.join(results_logs_path, "Othelloresukls_log" + str(i) + "_" + str(j) + ".csv")
                modelPath_first = os.path.join(model_logs_path, "OthelloState_model" + str(i) + ".pkl")
                modelPath_second = os.path.join(model_logs_path, "OthelloState_model" + str(j) + ".pkl")

                writer = csv.writer(open(results_path, 'w', newline='\n'))

                if not os.path.exists(csv_logs_path):
                    os.mkdir(csv_logs_path)
                if not os.path.exists(model_logs_path):
                    os.mkdir(model_logs_path)

                expert_clf = joblib.load(modelPath_first)
                clf = joblib.load(modelPath_second)

                num_of_games = int(10 * 2 / 2)
                wins = []
                for k in range(num_of_games):
                    wins.append(UCTPlayTestGame(classifier=clf, expert_clf=expert_clf, writer=None))
                    print(wins)
                    print("percentage = ", (wins.count("expert") + wins.count(0)) / len(wins))

                writer.writerow(["percentage = ", (wins.count("expert") + wins.count(0)) / len(wins)])
                win_rate[i][j] = wins.count("expert") / len(wins)

                np.save("1-30-5.npy", win_rate)

        self.assertEqual(True, os.path.exists("1-30-5.npy"))


if __name__ == '__main__':
    unittest.main()
