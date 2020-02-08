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
        self.depth = 3

    def getColumn(self, board):
        _, best_move = self.maximize(board, -math.inf, math.inf, 0)
        error("BEST MOVE")
        error(best_move)
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
                return alpha
            board_copy = deepcopy(board)
            board_copy.play(self.p2_id, col)
            new_beta, _ = self.maximize(board_copy, alpha, beta, level)
            if new_beta < beta:
                beta = new_beta
        return beta


    def get_score(self, board):
        list_board = board.board
        score = 0
        for i in range(board.num_rows):
            for j in range(board.num_cols):
                if list_board[j][i] == self.p1_id:
                    score += self.ref_table[i,j]
                elif list_board[j][i] == self.p2_id:
                    score -= self.ref_table[i,j]
        error(board)
        error(score)
        return score

    def is_checkmate(self, board):
        pass



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
