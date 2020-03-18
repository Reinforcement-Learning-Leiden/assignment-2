import hex_skeleton as HexBoard
from random import choice
from class_mcts import Node
import copy

_Cp = 1


def exploited_tree_policy(node):
    current_node = node
    while not current_node.is_terminal_node():
        if not current_node.is_fully_expanded():
            return current_node.expand()
        else:
            current_node = current_node.selectChildUCT()
    return current_node


def MCTS(board: HexBoard,color, itermax = 1000 ):
    #board.color = color
    rootnode = Node(state=board, color = color)

    for _ in range(0, itermax):
        v = exploited_tree_policy(rootnode)
        reward = v.playout()
        v.backpropagate(reward)
    # to select best child go for exploitation only
    return rootnode.selectChildUCT()

    # for i in range (itermax):
    #     node = rootnode # in each iteration the 4 actions are executed from the root
    #     state = copy.deepcopy(board) # deep copy instead of clone
    #
    #     # SELECT
    #     while node.untriedMoves == [] and node.children != []:
    #         node = node.selectChildUCT()
    #         state, color = state.DoMove(node, color) ###????????????
    #
    #     # EXPAND
    #     if node.untriedMoves != []: # we can expand node
    #         # m = choice(node.untriedMoves)
    #         # state, color = state.DoMove(m, color)
    #         # node = node.addChild(m,state) # add node m to the children of node state
    #         node = node.expand(color)
    #
    #     # PLAYOUT
    #     # while not node.is_terminal_node(): # state is nonterminal
    #     #     state.DoMove(choice(state.GetMoves()))
    #     reward = node.playout()
    #
    #     #BACKPROPAGATE
    #     while node != None:
    #         # node.update(state.getResult(node.moved))
    #         # node = node.parentNode
    #         node.backpropagate(reward)
    #
    # # return the best move
    # return sorted(rootnode.children, key= lambda c: c.visited)[-1].move




def _update_board(board: HexBoard, move, color) -> HexBoard:
    """
    Makes a deep copy of the board and updates the board state on that copy.
    This makes it so that we don't need to use an undo move function.
    The reason for using deepcopy is because python passes objects by reference
    if you use the "=" operator
    """
    board = copy.deepcopy(board)
    board.place(move, color)
    return board

