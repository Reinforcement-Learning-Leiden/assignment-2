import numpy as np
import ttid_alphabeta as tt
import trueskill as ts
import matplotlib.pyplot as plt
from play_hex import boardSize
from MCTS import MCTS
import time
from random import randint

from hex_skeleton import HexBoard

### GLOBALS ###
NUMBER_OF_GAMES: int = 200
# number of iterations for the MCTS algorithm. If MAX_SECONDS_MCTS != None this is ignored
itermax = [500]  # , 100, 500 #10, 50, 100,
# Choose the number of seconds MCTS is allowed to search, else None
MAX_SECONDS_MCTS = None
Cp = [0.1, 1, 2]
###############
start_time = time.time()


def main():

    for it in itermax:
        performance = []

        for c in Cp:
            counter_blue = 0
            counter_red = 0
            for match in range(NUMBER_OF_GAMES):

                board = HexBoard(boardSize)  # BOARD_SIZE_TTID
                num_of_cells = board.get_board_size() * board.get_board_size()

                for _ in range(int(num_of_cells/2)):

                    _, move_blue = MCTS(
                        board, board.BLUE, it, c, max_seconds=MAX_SECONDS_MCTS)
                    board.place(move_blue, board.BLUE)
                    board.print()
                    if board.is_game_over():

                        print("==== BLUE WINS ====")
                        board.print()
                        counter_blue += 1
                        break

                    move_rand = board.get_move_list()[randint(
                        0, len(board.get_move_list())-1)]  # Random player
                    board.place(move_rand, board.RED)
                    board.print()
                    if board.is_game_over():

                        print("==== RED WINS ====")
                        board.print()
                        counter_red += 1
                        break

            performance.append(counter_blue / NUMBER_OF_GAMES)

        objects = ("MCTS C=0.1", "MCTS C=1", "MCTS C=2")
        y_pos = np.arange(len(objects))
        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('win %')
        # f'MCTS vs Random at {it} iterations using C={c}'
        plt.title("MCTS performance vs random at varying params")
        plt.savefig(f"tuning_iter{it}.png")


if __name__ == '__main__':
    main()

 # _, move_red = MCTS(
    #     board, board.RED, it, c, max_seconds=MAX_SECONDS_MCTS)
    # board.place(move_red, board.RED)
    # board.print()
    # if board.is_game_over():

    #     print("==== RED WINS ====")
    #     board.print()
    #     red, blue = ts.rate_1vs1(red, blue)
    #     break
