import numpy as np
import ttid_alphabeta as tt
import trueskill as ts
import matplotlib.pyplot as plt
from play_hex import boardSize
from MCTS import MCTS
import time

from hex_skeleton import HexBoard

### GLOBALS ###
#BLUE_SEC_TO_THINK: int = 1
RED_SEC_TO_THINK: int = 3
NUMBER_OF_GAMES: int = 120
itermax = 3000 # number of iterations for the MCTS algorithm
MAX_SECONDS_MCTS = None #Choose the number of seconds MCTS is allowed to search, else None
Cp=1
###############
start_time=time.time()
bWins=0
rWins=0
def main():
    board = HexBoard(boardSize) #BOARD_SIZE_TTID
    num_of_cells = board.get_board_size() * board.get_board_size()


    for _ in range(int(num_of_cells/2)):

        best_node_blue, move_blue = MCTS(board, board.BLUE, itermax, Cp, max_seconds=MAX_SECONDS_MCTS)
        board.place(move_blue, board.BLUE)
        board.print()
        if board.is_game_over():

            print("==== BLUE WINS ====")
            board.print()
            return "blue"
        move_red = tt.iterative_deepening(
            board, is_max=True, max_seconds=RED_SEC_TO_THINK, depth_lim=15, show_AI=False)
        board.place(move_red, board.RED)
        board.print()
        if board.is_game_over():

            print("==== RED WINS ====")
            board.print()
            return "red"


if __name__ == '__main__':
    to_plot_x = []
    to_plot_blue = []
    to_plot_red = []
    plot_retrieved=[]
    plot_total_retrieved=[]


    # Create fresh ratings for both players
    blue = ts.Rating()
    red = ts.Rating()

    to_plot_x.append(0)
    to_plot_blue.append(blue.mu)
    to_plot_red.append(red.mu)

    for match in range(NUMBER_OF_GAMES):  # Play 12 games
        res = main()  # Main game loop
        if res == "blue":  # If blue won
            bWins = +1
            blue, red = ts.rate_1vs1(blue, red)

        elif res == "red":  # If red won
            red, blue = ts.rate_1vs1(red, blue)
            rWins = +1

            blue, red = ts.rate_1vs1(blue, red, drawn=True)

        to_plot_x.append(match)
        to_plot_blue.append(blue.mu)
        to_plot_red.append(red.mu)


    print('time to complete: '+ str(time.time()-start_time))
    print('out of '+str(NUMBER_OF_GAMES)+" Blue won: "+str(bWins)+" and Red won: "+str(rWins)+".")
    print("BLUE'S RANK: " + str(blue.mu))
    print("RED'S RANK: " + str(red.mu))
    plt.plot(to_plot_x, to_plot_blue)
    plt.plot(to_plot_x, to_plot_red)
    plt.xlabel("# of games")
    plt.ylabel("player rating")
    plt.savefig(f"idtt_ai_vs_ai_{np.random.randint(100)}.png")
