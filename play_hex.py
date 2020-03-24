
from hex_skeleton import HexBoard
from MCTS import MCTS


win_message_human = "******************************************\n\
*               YOU WIN                  *\n\
******************************************"

loss_message_human = "******************************************\n\
*              YOU LOSE                  *\n\
******************************************"

win_message_blue = "******************************************\n\
*               BLUE WINS                  *\n\
******************************************"

win_message_red = "******************************************\n\
*              RED WINS                  *\n\
******************************************"

# number of iterations for MCTS Algorithm
itermax = 1000


#TODO: test
def human_input(size_of_board):
    # TODO: This is fine, but we can add a try/catch block to make sure the user can't crash the main loop
    try:
        input_user = input("Your Turn: ")
        if ',' in input_user:
            x, y = input_user.split(',')
        else:
            x, y = input_user.split()
            x = int(x)
            y = int(y)
            if x in range(size_of_board) and y in range(size_of_board):
                coordinates = (x, y)
                return coordinates
            else:
                print('coordinates (', x, ',', y, ') are not in range')
                return
    except:
        print('please input the coordinates in the form of \'x,y\' or \'x y\'')
        return




#TODO: 
##########################################################
#        CODE BLOCK FOR HUMAN (RED) VS AI (BLUE)         #
##########################################################

def main_Human_AI(bSize):
    print('the program plays Blue(LeftToRight) and the user plays Red(UpToButtom)')
    board = HexBoard(bSize)
    num_of_cells = board.get_board_size() * board.get_board_size()
    for nc in range(int(num_of_cells/2)):
        move_human = human_input(board.get_board_size())
        while not move_human in board.get_move_list():
            print('move is not legal, please choose another cell')
            move_human = human_input(board.get_board_size())
        board.place(move_human, board.RED)
        board.print()
        if board.is_game_over(): 
            print(win_message_human)
            board.print()
            break
        print(f"AAHAHHH BOARD ={ board }")
        # change here: used to return a node, we want the move that leads to this node
        best_node, move_program = MCTS(board,board.BLUE,itermax)
        print("THIS SHOULD PRINT")
        board.place(move_program, board.BLUE)
        board.print()
        if board.is_game_over(): 
            print(loss_message_human)
            board.print()
            break

##########################################################
#               CODE BLOCK FOR AI VS AI                  #
##########################################################

def main_AI_AI(bSize):

    board = HexBoard(bSize)
    num_of_cells = board.get_board_size() * board.get_board_size()
    for nc in range(int(num_of_cells/2)):
        # ## Just a small heuristic for opening strategy, you can test this if you want. But then you have to comment the move_blue below out too
        #     if board.size % 2 != 0 and len(board.get_move_list()) == len(board.get_all_vertices()): # If it's the first move and the board is uneven
        #         move_blue = (board.size // 2, board.size // 2) # Always place the first move in the middle
        #     else:
        #         move_blue = MCTS.MCTS(board,board.BLUE, itermax)

            best_node_blue, move_blue = MCTS(board, board.BLUE, itermax)
            board.place(move_blue,board.BLUE)
            board.print()
            if board.is_game_over(): # TODO: add condition for game over without no winning (board full)
                print(win_message_blue)
                board.print()
            # break
                return "blue" #???
            best_node_red, move_red = MCTS(board, board.RED, itermax)
            board.place(move_red, board.RED)
            board.print()
            if board.is_game_over():  # TODO: add condition for game over without no winning (board full)
                print(win_message_red)
                board.print()
            # break
                return "red"


if __name__ == '__main__':
#     #call main for  AI-vs-AI or human-vs-AI
     main_Human_AI(4) #
     #main_Human_AI(4)





