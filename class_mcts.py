import hex_skeleton as HexBoard
import numpy as np
import math
import MCTS
import copy


class Node:

    def __init__(self, state: HexBoard,color, parent = None, visited=0, win =0): # TODO Color?
        self.state = state
        self.parent = parent
        self.visited = visited  # num of visits
        self.win = win # Not needed?
        self.children = [] #dict()
        self.untriedMoves_list = [] # NONE?
        self.color = color # the color that node plays



    # def setChildren(self):
    #     legal_moves = self.state.get_move_list()
    #     for move in legal_moves:
    #         sim_board = copy.deepcopy(self.state)
    #         sim_board.place(move, self.color)
    #         self.children.update({sim_board:{'win':0, 'visited':0}})

    def getChildren(self):
        return self.children


    def untriedMoves(self):
        """
        in the beginning, all the children are untried/unexpanded, as the procedure goes on, children are expanded onebyone
        """
        if len(self.untriedMoves_list) == 0:
            self.untriedMoves_list = self.state.get_move_list()
        return self.untriedMoves_list

    def is_fully_expanded(self):
        return len(self.untriedMoves()) == 0 # all moves are tried before


    # best_child
    def selectChildUCT(self)->HexBoard:
        # calculate UCT of all children and select the highest
        UCTs = []
        for i in range(len(self.children)):
            UCTs[i] =  (self.children[i].win/self.children[i].visited) + \
                      (MCTS._Cp * math.sqrt(np.log(self.visited/ self.children[i].visited)))

        best_state = self.children[np.argmax(UCTs)]
        return best_state

    # copied
    def playout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]


    # TODO: Fix color and test
    def expand(self, color):
        action = self.untriedMoves_list.pop()
        next_state, color = self.state.DoMove(action, color) # right color? when opponent?
        child_node = Node(next_state,color, parent=self) # child plays the opposite color
        self.children.append(child_node)
        return child_node


    def is_terminal_node(self):
        return self.state.is_game_over()

    def playout(self):
        # if self.state is None:
        #     print("state is none")
        #     return
        current_playout_state = copy.deepcopy(self.state)
        current_color = self.color
        # TODO: what is wrong with boardObject.is_game_over()?
        while not (current_playout_state.is_game_over()): # dict has no attribute is_game_over?
            possible_moves = current_playout_state.get_move_list()
            action = self.playout_policy(possible_moves)
            current_playout_state, current_color = current_playout_state.DoMove(action, current_color)# TODO: COLOR!!!!!
        return current_playout_state.check_win(self.color) #TODO: COLOR correct?

    def backpropagate(self, result):
        self.visited += 1
        if(result == 1):
            self.win +=1
        #self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)


