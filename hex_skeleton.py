import copy

class HexBoard:
    BLUE = 1
    RED = 2
    EMPTY = 3

    #cutoffs = 0
    #dCutoffs = 0  # cutoffs made by the aplphabeta with Dijkstra
    #d4Cutoffs = 0
    #rCutoffs = 0  # cutoffs made by the alphabeta with random eval
    #total_dCutoffs = 0
    #total_rCutoffs = 0
    #total_d4Cutoffs = 0

    #rTime = 0
    #dTime = 0
    #d4Time = 0

    def __init__(self, board_size):
        self.board = {}
        self.size = board_size
        self.game_over = False
        for x in range(board_size):
            for y in range(board_size):
                self.board[x, y] = HexBoard.EMPTY

    def is_game_over(self):
        return self.game_over

    def is_empty(self, coordinates):
        return self.board[coordinates] == HexBoard.EMPTY

    def is_color(self, coordinates, color):
        return self.board[coordinates] == color

    def get_color(self, coordinates):
        if coordinates == (-1, -1):
            return HexBoard.EMPTY
        return self.board[coordinates]

    def place(self, coordinates, color):
        if not self.game_over and self.board[coordinates] == HexBoard.EMPTY:
            self.board[coordinates] = color
            if self.check_win(HexBoard.RED) or self.check_win(HexBoard.BLUE):
                self.game_over = True

    def get_opposite_color(self, current_color):
        if current_color == HexBoard.BLUE:
            return HexBoard.RED
        return HexBoard.BLUE

    def get_neighbors(self, coordinates):
        (cx, cy) = coordinates
        neighbors = []
        if cx - 1 >= 0:
            neighbors.append((cx - 1, cy))
        if cx + 1 < self.size:
            neighbors.append((cx + 1, cy))
        if cx - 1 >= 0 and cy + 1 <= self.size - 1:
            neighbors.append((cx - 1, cy + 1))
        if cx + 1 < self.size and cy - 1 >= 0:
            neighbors.append((cx + 1, cy - 1))
        if cy + 1 < self.size:
            neighbors.append((cx, cy + 1))
        if cy - 1 >= 0:
            neighbors.append((cx, cy - 1))
        return neighbors

    def border(self, color, move):
        (nx, ny) = move
        return (color == HexBoard.BLUE and nx == self.size - 1) or (color == HexBoard.RED and ny == self.size - 1)

    def traverse(self, color, move, visited):
        if not self.is_color(move, color) or (move in visited and visited[move]):
            return False
        if self.border(color, move):
            return True
        visited[move] = True
        for n in self.get_neighbors(move):
            if self.traverse(color, n, visited):
                return True
        return False

    def check_win(self, color):
        for i in range(self.size):
            if color == HexBoard.BLUE:
                move = (0, i)
            else:
                move = (i, 0)
            if self.traverse(color, move, {}):
                return True
        return False

    def print(self):
        print("   ", end="")
        for y in range(self.size):
            print(chr(y + ord('a')), "", end="")
        print("")
        print(" -----------------------")
        for y in range(self.size):
            print(y, "|", end="")
            for z in range(y):
                print(" ", end="")
            for x in range(self.size):
                piece = self.board[x, y]
                if piece == HexBoard.BLUE:
                    print("b ", end="")
                elif piece == HexBoard.RED:
                    print("r ", end="")
                else:
                    if x == self.size:
                        print("-", end="")
                    else:
                        print("- ", end="")
            print("|")
        print("   -----------------------")

    ############################################
    #              CUSTOM                      # #
    ############################################   #
    #              METHODS                     # #
    ############################################

    def get_move_list(self):
        move_list = []
        for i, p in self.board:
            if self.is_empty((i, p)):
                move_list.append((i, p))
        return move_list

    def get_all_vertices(self):
        vertex_set = []
        for i, p in self.board:
            vertex_set.append((i, p))
        return vertex_set

    def get_borders(self, color):
        borders = []
        for i, p in self.board:
            if self.border(color, (i, p)):
                borders.append((i, p))
        return borders

    def undo_move(self, coordinates):
        self.board[coordinates] = HexBoard.EMPTY

    def get_board_size(self):
        return self.size

    
    def DoMove(self, move,color):
        if move not in self.get_move_list():
            raise ValueError(
                "move {0} on board {1} is not legal".format(move, self.board)
            )
        #NOTE: If you want to make a new hexboard object, you have to make a deepcopy, or else you just reference the same object.
        new_state = copy.deepcopy(self)  # a new hex_board created to retain the board and the functions for the expanded child
        # new_state = self.place(move, color) #NOTE: THIS IS WRONG, board.place() does not return anything!!
        new_state.place(move,color) 
        #FIXME: Now that this works, we can see the next error: ValueError: attempt to get argmax of an empty sequence
        # This is our next step then! :)
        color = self.get_opposite_color(color)

        return new_state,color
