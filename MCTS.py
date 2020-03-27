import hex_skeleton as HexBoard
from random import choice
from class_mcts import Node
import copy
import time

#_Cp = 0


def exploited_tree_policy(node: Node, color):
    # copy.deepcopy(node) # if copied, does it retain the children?
    current_node = node
    current_action = None  # used to keep the action that leads to the best childnode
    #print(f"CURRENT NODE in 'exploited_tree_policy' method: {current_node}")
    # while travesring the tree, if the selected node not fully expanded, expand one child, if fully expanded select one child
    while not current_node.is_terminal_node():
        if not current_node.is_fully_expanded():
            return current_node.expand(color)
        else:
            current_node, current_action = current_node.selectChildUCT()
    return current_node, current_action


def MCTS(board: HexBoard, color, itermax=1000, Cp = 1, max_seconds=None):
    #board.color = color
    rootnode = Node(state=board, color=color, _Cp = Cp)
    t = time.time()

    if max_seconds is not None:
        while not time.time() - t >= max_seconds:
            # select and expand
            # v = node, a = action that leads to node v
            v, a = exploited_tree_policy(rootnode, color)
            # playout
            reward = v.playout()
            # backpropagate
            v.backpropagate(reward)
            # to select best child go for exploitation only
            # returns (bestnode, bestmove)
        print("time to calculate best action in time mode: ", str(time.time()-t))
        return rootnode.selectChildUCT()
    else:  # if max_seconds is None (not provided by the user), run the algorithm by itermax
        for _ in range(0, itermax):
            # select and expand
            # v = node, a = action that leads to node v
            v, a = exploited_tree_policy(rootnode, color)
            # playout
            reward = v.playout()
            # backpropagate
            v.backpropagate(reward)
        # to select best child go for exploitation only
        # returns (bestnode, bestmove)
        print("time to calculate best action in iteration mode: ",
              str(time.time() - t))
        # best_state_found, _ = rootnode.selectChildUCT()
        # print(best_state_found.win / best_state_found.visited)
        return rootnode.selectChildUCT()
