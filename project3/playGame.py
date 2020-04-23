'''Created by nomanshafqat at 2020-02-18'''
from UCT import OthelloState, UCT, get_state
import os
import numpy as np
import time


#plays one game based on UCT algorithm for training
def UCTPlayGame(classifier=None, classifier2=None,Wins=[], Game_logs=[]):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = OthelloState(8)  # uncomment to play Othello on a square board of the given size
    all_moves=[]
    time_start = time.time()
    # print("game_begin")

    while (state.GetMoves() != []):

        if state.playerJustMoved == 1:
            if classifier!=None:
                m = UCT(rootstate=state, itermax=1000, verbose=False, classifier=classifier)
            else:
                m = UCT(rootstate=state, itermax=100, verbose=False, classifier=classifier)
        else:
            m = UCT(rootstate=state, itermax=1000, verbose=False,
                    classifier=classifier2)  # play with values for itermax and verbose = True

        game_str = get_state(state)
        game_str.append(str(m[0]) + "_" + str(m[1]))
        all_moves.append(game_str)
        state.DoMove(m)

    print("\n time (s)= ", time.time() - time_start)
    return_value=None
    if state.GetResult(state.playerJustMoved) == 1.0:
        if state.playerJustMoved == 2:
            print("Player " + str(state.playerJustMoved) + " expert", " wins!")
            return_value= "expert"
        else:
            print("Player " + str(state.playerJustMoved) + " apprentice", " wins!")
            return_value= "apprentice"

    elif state.GetResult(state.playerJustMoved) == 0.0:
        if state.playerJustMoved == 2:
            print("Player " + str(state.playerJustMoved) + " apprentice", " wins!")
            return_value= "apprentice"
        else:
            print("Player " + str(state.playerJustMoved) + " expert", " wins!")
            return_value= "expert"

    else:
        print("Nobody wins!")
        return_value=0

    # print(return_value,len(all_moves))

    Wins.append(return_value)
    Game_logs.append(all_moves)
    return (return_value,all_moves)

