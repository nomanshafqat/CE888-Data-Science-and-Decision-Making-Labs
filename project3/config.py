'''Created by nomanshafqat at 2020-04-02'''

from os import path , mkdir
config={}


config["target_dir"]="Logs"
# config["iteration"]=open("iteration_no.txt").readline()
config["total_iterations"]=21



if not path.exists(config["target_dir"]):
    mkdir(config["target_dir"])
