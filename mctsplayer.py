from player import Player
from MCTS_agent import ConnectTree, MCTreeSearch
from alphabeta import AlphabetaPlayer
# from board import Board
from copy import deepcopy
from random import shuffle
from math import inf
from logging import error, warning
# import numpy as np
# import time

class AIPlayer(Player):

    def __init__(self):
        self.name = ""
        self.p1_id = -1 # -1 if 2nd player
        self.p2_id = 1
        self.ref_table = [[3,4,5,7,5,4,3],[4,6,8,10,8,6,4],[5,8,11,13,11,8,5],[5,8,11,13,11,8,5],[4,6,8,10,8,6,4],[3,4,5,7,5,4,3]]
        self.depth = 5

    def getColumn(self, board):
        # t0 = time.time()
        tree = MCTreeSearch(tag=1, exploration_factor=1)
        for i in range(7):
            num_vis = getattr(getattr(tree.play_tree, 'm' + str(i + 1)), 'num_visit')
            num_w = getattr(getattr(tree.play_tree, 'm' + str(i + 1)), 'num_win')
            print('-----------')
            print('move:', i)
            print('visits', num_vis)
            print('wins', num_w)
            moves = tree.available_moves(tree.play_tree.state)

        # error("BEST MOVE"+str(best_move))
        # warning(time.time() - t0)

        return best_move


    def get_score(self, board):
        checkmate = self.is_checkmate(board)
        if checkmate:
            return checkmate

        # error(board)
        list_board = board.board
        score = 0
        for i in range(board.num_rows):
            for j in range(board.num_cols):
                score += list_board[j][i] * self.ref_table[i][j] * self.p1_id
        return score

    def test_win(self, list):
        for i in range(len(list)-3):
            if [self.p2_id]*4 == list[i:i+4]:
                # warning("ADV CHECKMATE")
                return -inf
            elif [self.p1_id]*4 == list[i:i+4]:
                # warning("MY CHECKMATE")
                return inf

    def is_checkmate(self, board): # TODO when p1 finds checkmate he ignores p2 checkmates
        for c in range(board.num_cols):
            col = board.getCol(c)
            val = self.test_win(col)
            if val: return val

        up = True
        for shift in range(-2,4): # TODO generalize for num_cols
            diag = board.getDiagonal(up,shift)
            val = self.test_win(diag)
            if val: return val

        up = False
        for shift in range(3,9): # Downwards diags
            diag = board.getDiagonal(up,shift)
            val = self.test_win(diag)
            if val: return val

        for r in range(board.num_rows):
            row = board.getRow(r)
            # print(row)
            val = self.test_win(row)
            if val: return val

