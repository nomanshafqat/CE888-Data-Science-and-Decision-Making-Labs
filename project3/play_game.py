'''Created by nomanshafqat at 2020-02-18'''
from UCT import OthelloState, UCT, get_state
import os
import numpy as np


def UCTPlayGame(writer=None, classifier=None, classifier2=None):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = OthelloState(8)  # uncomment to play Othello on a square board of the given size

    while (state.GetMoves() != []):
        print(".", end=" ")
        # print(str(state))
        # print(state.get_state())
        # print(state.playerJustMoved)

        if state.playerJustMoved == 1:
            m = UCT(rootstate=state, itermax=24, verbose=False,
                    classifier=classifier2)  # play with values for itermax and verbose = True
        else:
            m = UCT(rootstate=state, itermax=30, verbose=False, classifier=classifier)

        game_str = get_state(state)
        game_str.append(str(m[0]) + "_" + str(m[1]))

        if writer != None:
            writer.writerow(game_str)

        state.DoMove(m)
    if state.GetResult(state.playerJustMoved) == 1.0:
        print("Player " + str(state.playerJustMoved) + " wins!")
        return str(state.playerJustMoved)
    elif state.GetResult(state.playerJustMoved) == 0.0:
        print("Player " + str(3 - state.playerJustMoved) + " wins!")
        return str(3 - state.playerJustMoved)
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
