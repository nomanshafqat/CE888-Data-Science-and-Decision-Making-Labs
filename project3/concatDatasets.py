'''Created by nomanshafqat at 4/23/20'''
import os
import pandas as pd

# Concats the datasets from itertaion (1 to n-1) or just (n-1) based on break_ and
# returns concatenated dataset
def concatAllDatasets(csv_logs_path, i, break_=False):
    whole_data = None
    #loop to iterate over all the logs from 0 to n in reversed order
    for j in reversed(range(0, i + 1)):
        csvPath = os.path.join(csv_logs_path, "OthelloState_log" + str(j) + ".csv")
        print(j, csvPath)
        dataset_ = pd.read_csv(csvPath, header=None,delimiter = ",")

        if str(type(whole_data)) == "<class 'NoneType'>":
            whole_data = dataset_.copy()
        else:
            whole_data = whole_data.append(dataset_)
        if break_==True:
            break

    return whole_data