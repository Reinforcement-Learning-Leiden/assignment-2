import time
import random
import numpy as np
from hex_skeleton import HexBoard


class TranspositionTable:
    BLUE = 1
    RED = 2
    EMPTY = 3
    retrievedStates=0
    total_retrievedStates=0
    #cutoffs=0
    #total_cutoffs=0

    def __init__(self, board: HexBoard):
        self.board = board
        self.zobTable = [[[random.randint(1, 2 ** 64 - 1) for i in range(2)] for j in range(self.board.size)] for k in
                         range(self.board.size)]
        # self.tbl_size = 2 ** 20  # experimental, can be changed
        self.dict = {}

    # ZOBRIST HASHING

    def indexing(self, piece):
        ''' mapping colors to a particular number'''
        if (piece == self.board.BLUE):
            # return 1
            return 0
        if (piece == self.board.RED):
            # return 2
            return 1
        else:
            return -1
            # return 2

    # each time a move is made on our board, whether during game play or alpha beta search we simply update the Zobrist Hash:
    def computeHash(self, board):
        h = 0
        for i, p in board.get_all_vertices():
            if not board.is_empty((i, p)):
                piece = self.indexing((i, p))
                h ^= self.zobTable[i][p][piece]
        return h

    def store(self, board, heuristic_val, depth, bestmove):
        self.hashValue = self.computeHash(board)
        self.dict[self.hashValue] = {
            "board": self.board, "val": heuristic_val, "depth": depth, "bm": bestmove}

    def lookup(self, board, depth):
        hit = False
        d_flag = False
        hash_v = self.computeHash(board)
        if hash_v in self.dict:
            if depth <= self.dict[hash_v]["depth"]:
                hit = True
                d_flag = True
                # print("lookup true", hash_v, hit, self.dict)
                return hit, self.dict[hash_v]["val"], self.dict[hash_v]["bm"], d_flag
            # return ttbm regardless of depth matching
            return hit, self.dict[hash_v]["val"], self.dict[hash_v]["bm"], d_flag
        return hit, None, None, d_flag
