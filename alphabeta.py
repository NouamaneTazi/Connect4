from player import Player
# from board import Board
from copy import deepcopy
from random import shuffle
from math import inf
from logging import error, warning
# import numpy as np
import time

class AlphabetaPlayer(Player):

    def __init__(self, depth = 5, plays_first=True):
        self.name = ""
        self.my_id = 1 if plays_first else -1 # -1 if 2nd player
        self.adv_id = -1 if plays_first else 1
        self.ref_table = [[3,4,5,7,5,4,3],[4,6,8,10,8,6,4],[5,8,11,13,11,8,5],[5,8,11,13,11,8,5],[4,6,8,10,8,6,4],[3,4,5,7,5,4,3]]
        self.depth = depth

    def getColumn(self, board):
        t0 = time.time()
        _, best_move = self.maximize(board, -inf, inf, 0)
        # error("BEST MOVE"+str(best_move))
        warning(time.time() - t0)
        # print("#"*40)
        # print("#"*40 + "\n")
        return best_move

    def maximize(self, board, alpha, beta, level):
        level+=1
        best_move = None
        if level == self.depth:
            return self.get_score(board), None
        possible_cols = board.getPossibleColumns()
        shuffle(possible_cols)
        for col in possible_cols: # p1 moves (o)
            if alpha >= beta:
                return alpha, best_move
            board_copy = deepcopy(board)
            row = board_copy.play(self.my_id, col)
            # checkmate = self.is_checkmate(board_copy)
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

        if best_move==None and level==1: error("I LOST")
        return alpha, best_move


    def minimize(self, board, alpha, beta, level):
        level+=1
        if level == self.depth:
            return self.get_score(board)
        possible_cols = board.getPossibleColumns()
        shuffle(possible_cols)
        for col in possible_cols: # p2 moves (x)
            if alpha >= beta:
                return beta
            board_copy = deepcopy(board)
            row = board_copy.play(self.adv_id, col)
            # checkmate = self.is_checkmate(board_copy)
            checkmate = self.getWinner(board_copy, (col,row))
            if checkmate:
                return checkmate
            new_beta, _ = self.maximize(board_copy, alpha, beta, level)
            if new_beta < beta:
                beta = new_beta
        return beta



    def get_score(self, board):
        # error(board)
        list_board = board.board
        score = 0
        for i in range(board.num_rows):
            for j in range(board.num_cols):
                score += list_board[j][i] * self.ref_table[i][j] * self.my_id
        return score


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


    def test_win(self, list):
        for i in range(len(list)-3):
            if [self.adv_id]*4 == list[i:i+4]:
                # warning("ADV CHECKMATE")
                return -inf
            elif [self.my_id]*4 == list[i:i+4]:
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

