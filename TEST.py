from player import Player
from board import Board
from copy import deepcopy
import random as rd
import math
from logging import error
import numpy as np

class AIPlayer(Player):

    def __init__(self):
        self.name = ""
        self.p1_id = -1
        self.p2_id = 1
        self.ref_table = np.array([[3,4,5,7,5,4,3],[4,6,8,10,8,6,4],[5,8,11,13,11,8,5],[5,8,11,13,11,8,5],[4,6,8,10,8,6,4],[3,4,5,7,5,4,3]])
        self.depth = 4
        self.depth = 4
        self.depth = 4

    def getColumn(self, board):
        _, best_move = self.maximize(board, -math.inf, math.inf, 0)
        # error("BEST MOVE = "+str(best_move))
        return best_move


    def maximize(self, board, alpha, beta, level):
        level+=1
        if level == self.depth:
            return self.get_score(board), None
#rd.choice(possible_cols)
        for col in board.getPossibleColumns(): # p1 moves TODO add shuffle
            if alpha >= beta:
                return alpha
            board_copy = deepcopy(board)
            board_copy.play(self.p1_id, col)
            new_alpha = self.minimize(board_copy, alpha, beta, level)
            if new_alpha > alpha:
                alpha = new_alpha
                best_move = col
        return alpha, best_move


    def minimize(self, board, alpha, beta, level):
        level+=1
        if level == self.depth:
            return self.get_score(board)

        for col in board.getPossibleColumns(): # p2 moves
            if alpha >= beta:
                return beta
            board_copy = deepcopy(board)
            board_copy.play(self.p2_id, col)
            new_beta, _ = self.maximize(board_copy, alpha, beta, level)
            if new_beta < beta:
                beta = new_beta
        return beta


    def get_score(self, board):
        checkmate = self.is_checkmate(board)
        if checkmate:
            # error("*"*20)
            # error(board)
            # error(checkmate)
            return checkmate

        list_board = board.board
        score = 0
        for i in range(board.num_rows):
            for j in range(board.num_cols):
                if list_board[j][i] == self.p1_id:
                    score += self.ref_table[i,j]
                elif list_board[j][i] == self.p2_id:
                    score -= self.ref_table[i,j]
        # error(board)
        # error(score)
        return score

    def test_win(self, list):
        for i in range(len(list)-4):
            if [1,1,1,1] == list[i:i+4]:
                return -math.inf
            elif [-1,-1,-1,-1] == list[i:i+4]:
                return math.inf

    def is_checkmate(self, board):
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
        for shift in range(3,10): # Downwards diags
            diag = board.getDiagonal(up,shift)
            val = self.test_win(diag)
            if val: return val

        for r in range(board.num_rows):
            row = board.getRow(r)
            val = self.test_win(row)
            if val: return val

    """def alpha_beta(self, board, player, alpha, beta, level): #explore branches
        if level >= self.depth:
            score = self.get_score(board)
            error(board)
            error(score)
            return player, alpha, beta, level, score
        level+=1
        error("LEVEL :"+str(level))
        player = - player
        possible_cols = board.getPossibleColumns()
        for col in possible_cols: # player move
            board_copy = deepcopy(board)
            board_copy.play(player, col)
            _, alpha, beta, _, score = self.alpha_beta(board_copy, player, alpha, beta, level)
            if player == self.p1_id: #maximize
                if score > alpha:
                    error(str(alpha)+" , "+str(beta))
                    alpha = score
                    error("#"*20)
                    error(str(alpha)+" , "+str(beta))
            elif player == self.p2_id: #minimize
                if score < beta:
                    error(str(alpha)+" , "+str(beta))
                    beta = score
                    error("#"*20)
                    error(str(alpha)+" , "+str(beta))

        return player, alpha, beta, level, score"""
