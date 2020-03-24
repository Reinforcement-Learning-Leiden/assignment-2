import hex_skeleton as HexBoard
import numpy as np
import math
import MCTS
import copy


class Node:

    def __init__(self, state: HexBoard,color, parent = None, visited=0, win =0): # TODO Color?
        print(f"INITIALIZATION WITH STATE = {state}")
        self.state = state
        self.parent = parent
        self.visited = visited  # num of visits
        self.win = win # Not needed?
        self.children = [] #dict()
        self.untriedMoves_list = None # Needs to be None to distinguish between initial state and when all moves tried
        self.color = color # the color that node plays



    # def setChildren(self):
    #     legal_moves = self.state.get_move_list()
    #     for move in legal_moves:
    #         sim_board = copy.deepcopy(self.state)
    #         sim_board.place(move, self.color)
    #         self.children.update({sim_board:{'win':0, 'visited':0}})

    #def getChildren(self):
    #    return self.children


    def untriedMoves(self):
        """
        in the beginning, all the children are untried/unexpanded, as the procedure goes on, children are expanded onebyone
        """
        if self.untriedMoves_list is None:
            self.untriedMoves_list = self.state.get_move_list()
        return self.untriedMoves_list

    def is_fully_expanded(self):
        return len(self.untriedMoves()) == 0 # all moves are tried before


    # best_child
    def selectChildUCT(self)->HexBoard:
        # calculate UCT of all children and select the highest
        UCTs = []
        for i in range(len(self.children)):
            #UCTs[i] =  (self.children[i].win/self.children[i].visited) + \
            #          (MCTS._Cp * math.sqrt(np.log(self.visited/ self.children[i].visited)))
            
            # children is a list of tuples (childnode, action). To get the child node children[i][0] is used
            UCTs.append((self.children[i][0].win / self.children[i][0].visited) + \
                      (MCTS._Cp * math.sqrt(np.log(self.visited / self.children[i][0].visited))))

        best_state, best_action = self.children[np.argmax(UCTs)]
        return best_state, best_action

    # CHANGE HERE
    def playout_policy(self, possible_moves):
        if len(possible_moves) <= 1:
            return possible_moves[0]
        else:
            return possible_moves[np.random.randint(len(possible_moves))]  # randit returns a random int between [low,high) -> lower-bound inclusive & higher-bound exclusive


    # TODO: Fix color and test
    def expand(self, color):
        action = self.untriedMoves_list.pop()
        # FIXME: DoMove() method is currently NOT returning the appropriate next state
        next_state, color = self.state.DoMove(action, color) # right color? when opponent?
        print(f"IS COLOR WORKING? {color}")
        print(f"Next state in method 'expand' = {next_state}") # The issue lies here, next state is null
        child_node = Node(next_state,color, parent=self) # child plays the opposite color
        print("Print me after the child node is created")
        self.children.append((child_node,action))
        return child_node, action


    def is_terminal_node(self):
        return self.state.is_game_over()

    def playout(self):
        # if self.state is None:
        #     print("state is none")
        #     return
        current_playout_state = copy.deepcopy(self.state)
        print(f"CURRENT PLAYOUT: {self.state}")
        current_color = self.color
        
        while not (current_playout_state.is_game_over()): 
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



