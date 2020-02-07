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
        self.columns = None
        self.p1_id = -1
        self.p2_id = 1
        self.ref_table = np.array([[3,4,5,7,5,4,3],[4,6,8,10,8,6,4],[5,8,11,13,11,8,5],[5,8,11,13,11,8,5],[4,6,8,10,8,6,4],[3,4,5,7,5,4,3]])
        self.depth = 2

    def getColumn(self, board):
        self.columns = board.getPossibleColumns()
        self.main(board)
        if self.columns:
            return rd.choice(self.columns)

    def main(self, board):
        alpha, beta = -math.inf, math.inf
        player = self.p2_id
        player, alpha, beta, level, score = self.alpha_beta(board, player, alpha, beta, 0)


    def alpha_beta(self, board, player, alpha, beta, level): #explore branches
        if level >= self.depth:
            score = self.get_score(board)
            error(board)
            error(score)
            return player, alpha, beta, level, score
        level+=1
        error("LEVEL :"+str(level))
        player = - player
        for col in self.columns: # player move
            board_copy = deepcopy(board)
            board_copy.play(player, col)
            _, alpha, beta, _, score = self.alpha_beta(board_copy, player, alpha, beta, level)
            if player == self.p1_id: #maximize
                if score > alpha:
                    error(str(alpha)+" , "+str(beta))
                    alpha = score
                    error("*"*20)
                    error(str(alpha)+" , "+str(beta))
            elif player == self.p2_id: #minimize
                if score < beta:
                    error(str(alpha)+" , "+str(beta))
                    beta = score
                    error("*"*20)
                    error(str(alpha)+" , "+str(beta))

        return player, alpha, beta, level, score

    def get_score(self, board):
        list_board = board.board
        score = 0
        for i in range(board.num_rows):
            for j in range(board.num_cols):
                if list_board[j][i] == self.p1_id:
                    score += self.ref_table[i,j]
                elif list_board[j][i] == self.p2_id:
                    score -= self.ref_table[i,j]
        return score

