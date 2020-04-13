'''Created by nomanshafqat at 2020-02-18'''
from UCT import OthelloState, UCT, get_state
import os
import numpy as np
import time

def UCTPlayGame(writer=None, classifier=None, classifier2=None):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = OthelloState(6)  # uncomment to play Othello on a square board of the given size

    time_start=time.time()
    expert=0
    import random
    rand=random.randint(1,10)/10

    if rand>0.5:
        expert=1
    else:
        expert=2
    print("expert=",expert)
    while (state.GetMoves() != []):
        print(".", end=" ")
        # print(str(state))
        # print(state.get_state())
        # print(state.playerJustMoved)

        if state.playerJustMoved == expert:

            m = UCT(rootstate=state, itermax=30, verbose=False, classifier=classifier)

        else:
            # print("\nexpert = ",expert)
            m = UCT(rootstate=state, itermax=30, verbose=False,
                    classifier=classifier2)  # play with values for itermax and verbose = True

        game_str = get_state(state)
        game_str.append(str(m[0]) + "_" + str(m[1]))

        if state.playerJustMoved==3-expert:
            if writer != None:
                writer.writerow(game_str)

        state.DoMove(m)
    print("\n time (s)= ",time.time()-time_start)

    if state.GetResult(state.playerJustMoved) == 1.0:
        if state.playerJustMoved==expert:
            print("Player " + str(state.playerJustMoved)+ " expert" , " wins!")
            return "expert"
        else:
            print("Player " + str(state.playerJustMoved)+ " apprentice" , " wins!")
            return "apprentice"

    elif state.GetResult(state.playerJustMoved) == 0.0:
        if state.playerJustMoved==expert:
            print("Player " + str(state.playerJustMoved)+ " apprentice" , " wins!")
            return "apprentice"
        else:
            print("Player " + str(state.playerJustMoved)+ " expert" , " wins!")
            return "expert"

    else:
        print("Nobody wins!")
        return 0


if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players.
    """
    num_of_games = 1000
    wins = []
    for i in range(num_of_games):
        wins.append(UCTPlayGame(classifier=None))
        print(wins)
