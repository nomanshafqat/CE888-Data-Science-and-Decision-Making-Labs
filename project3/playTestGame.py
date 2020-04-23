'''Created by nomanshafqat at 2020-04-07'''
import time

from UCT import OthelloState, UCT, get_state


#plays games for testing
def UCTPlayTestGame(writer=None, classifier=None, expert_clf=None):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = OthelloState(8)  # uncomment to play Othello on a square board of the given size

    time_start=time.time()
    expert=2
    while (state.GetMoves() != []):
        print(".", end=" ")

        if state.playerJustMoved == expert:
            m = UCT(rootstate=state, itermax=1000, verbose=False, classifier=classifier)
        else:
            m = UCT(rootstate=state, itermax=1000, verbose=False,
                    classifier=expert_clf)  # play with values for itermax and verbose = True
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
