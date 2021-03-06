from player import Player
# from board import Board
from copy import deepcopy
from random import shuffle
from math import inf
# from logging import error, warning
# import numpy as np
# import time

class AlphabetaPlayer(Player):
    """
    Si l'ordi est suffisamment rapide, on peut tenter d'augmenter le max_level à 6
    pour qu'il anticipe encore un autre coup
    """
    def __init__(self, max_level = 5, plays_first=True, heuristic=True):
        self.name = "Nouamane Tazi"
        self.my_id = 1 if plays_first else -1 # -1 if 2nd player
        self.adv_id = -1 if plays_first else 1
        self.ref_table = [[3,4,5,7,5,4,3],[4,6,8,10,8,6,4],[5,8,11,13,11,8,5],[5,8,11,13,11,8,5],[4,6,8,10,8,6,4],[3,4,5,7,5,4,3]]
        self.max_level = max_level
        self.heuristic = heuristic

    def getColumn(self, board):
        # t0 = time.time()
        _, best_move = self.maximize(board, -inf, inf, 0)
        # error("BEST MOVE"+str(best_move))
        # warning(time.time() - t0)
        # print("#"*40)
        # print("#"*40 + "\n")
        return best_move

    def maximize(self, board, alpha, beta, level):
        level+=1
        best_move = None
        if level == self.max_level:
            return self.get_score(board), None
        possible_cols = board.getPossibleColumns()
        shuffle(possible_cols)
        for col in possible_cols: # p1 moves (o)
            if alpha >= beta:
                return alpha, best_move
            board_copy = deepcopy(board)
            row = board_copy.play(self.my_id, col)
            checkmate = self.getWinner(board_copy, (col,row))
            if checkmate:
                return checkmate, col
            new_alpha = self.minimize(board_copy, alpha, beta, level)
            if new_alpha > alpha:
                alpha = new_alpha
                best_move = col
            if level==1:
                pass
                # print('='*4)
                # print("BRANCH : %d" % col)
                # print("alpha, beta = %.0f, %.0f" % (alpha,beta) )
                # print()

        if best_move==None and level==1:
            # print("I LOST")
            best_move = possible_cols[0]
        return alpha, best_move


    def minimize(self, board, alpha, beta, level):
        level+=1
        if level == self.max_level:
            return self.get_score(board)
        possible_cols = board.getPossibleColumns()
        shuffle(possible_cols)
        for col in possible_cols: # p2 moves (x)
            if alpha >= beta:
                return beta
            board_copy = deepcopy(board)
            row = board_copy.play(self.adv_id, col)
            checkmate = self.getWinner(board_copy, (col,row))
            if checkmate:
                return checkmate
            new_beta, _ = self.maximize(board_copy, alpha, beta, level)
            if new_beta < beta:
                beta = new_beta
        return beta



    def get_score(self, board):
        # error(board)
        if not self.heuristic: return 0
        list_board = board.board
        double_list = [[list_board[j][i] * self.ref_table[i][j] * self.my_id for i in range(board.num_rows)]
                    for j in range(board.num_cols)]
        return sum(sum(double_list,[]))


    def getWinner(self, board, pos):
        """Returns the player (boolean) who won, or None if nobody won"""
        tests = []
        tests.append(board.getCol(pos[0]))
        tests.append(board.getRow(pos[1]))
        tests.append(board.getDiagonal(True, pos[0] - pos[1]))
        tests.append(board.getDiagonal(False, pos[0] + pos[1]))
        for test in tests:
            player_id, size = self.longest_seq(test)
            if size >= 4: return self.my_id * player_id * inf
    

    def longest_seq(self, seq):
        """Find the longuest sequence values (different from 0) in a list"""
        best = (None, 0)
        curr = (None, 0)  # the value of the sequence, and its size
        for v in seq:
            if not v:
                curr = (None, 0)
            else:
                count = (v == curr[0]) * curr[1] + 1
                curr = (v, count)

            if curr[1] > best[1]:
                best = curr
        return best
