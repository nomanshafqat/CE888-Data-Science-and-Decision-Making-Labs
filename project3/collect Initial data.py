'''Created by nomanshafqat at 2020-02-18'''
from UCT import OthelloState, UCT


def UCTPlayGame():
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = OthelloState(8)  # uncomment to play Othello on a square board of the given size
    # state = OXOState() # uncomment to play OXO
    # state = NimState(15)  # uncomment to play Nim with the given number of starting chips
    a = 0
    while (state.GetMoves() != []):
        print(a)
        a += 1
        # print(str(state))
        # print(state.get_state())
        # print(state.playerJustMoved)

        if state.playerJustMoved == 1:
            m = UCT(rootstate=state, itermax=1000, verbose=False)  # play with values for itermax and verbose = True
        else:
            m = UCT(rootstate=state, itermax=1000, verbose=False)

        import csv
        writer = csv.writer(open(str(state.size)+"_"+ state.__class__.__name__ + ".csv", 'a',newline='\n'))
        # writer.writerows(someiterable)

        game_str = []
        # print(state.size, state.playerJustMoved)
        # game_str += str(state.size) + "," + str(state.playerJustMoved)

        game_str.append(str(state.playerJustMoved))

        for i in range(state.size):
            for j in range(state.size):
                # print(state.board[i][j], end=" ")
                # game_str+=","+str(state.board[i][j] )

                game_str.append(str(state.board[i][j]))
            # print("", end="\n")

        # game_str += "," + str(m[0])+"_"+str(m[1])

        game_str.append(str(m[0]) + "_" + str(m[1]))
        # print("Best Move: " + str(m) + "\n")

        # print(game_str)

        # if state.playerJustMoved == 1:
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
    num_of_games=1000
    wins=[]
    for i in range(num_of_games):

        wins.append(UCTPlayGame())
        print(wins)


