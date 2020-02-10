from player import Player
from MCTS import Agent, Node
from numpy import argmax

class MCTSPlayer(Player):

    def __init__(self, plays_first):
        self.name = ""
        self.plays_first = plays_first

    def getColumn(self, board):
        # t0 = time.time()
        depth = 0 if self.plays_first else 1
        node = Node(board=board, depth=depth)
        Agent().train_mcts_ntimes(node, 10, verbose=True)
        best_move = argmax([child.wins for child in node.children])
        print("#"*50)
        # warning(time.time() - t0)
        return best_move
