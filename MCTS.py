import numpy as np
from alphabeta import AlphabetaPlayer
from copy import deepcopy
import random

class Node: # an explored board
    def __init__(self, board, parent, first_win=0):
        self.board = board
        self.children = [] # [Nodes]
        self.parent = parent # Node
        self.wins = first_win
        self.games = 1

    def get_uct(self):
        if self.games == 0:
            return None
        return (self.wins / self.games) + np.sqrt(2 * np.log(self.parent.games) / self.games)


class Agent: #Suppose im player 1
    def __init__(self, board):
        self.board = board

    def simulate(self, board):
        p1 = AlphabetaPlayer(depth=2, plays_first=True)
        p2 = AlphabetaPlayer(depth=2, plays_first=False)
        while True:
            # try except return 0 ?
            p1_move = p1.getColumn(board)
            if p1_move: board.play(1, p1_move)
            else: return 0 # p2 WINS

            p2_move = p2.getColumn(board)
            if p2_move: board.play(1, p2_move)
            else: return 1 # p1 WINS

    def train_mcts_once(self, root_node):
        # selection
        node = root_node
        while len(node.children) > 0:
            ucts = [child.get_uct() for child in node.children]
            if None in ucts:
                node = random.choice(node.children)
            else:
                node = node.children[np.argmax(ucts)]

        # expansion
        possible_moves = node.board.getPossibleColumns()
        if len(possible_moves) > 0: # not a terminal node
            node_board = deepcopy(node.board)
            children_boards = [node_board.play(player, move) for move in possible_moves]

            # simulation
            children_wins = [self.simulate(board) for board in children_boards] #[1,0,1,0,..]
            node.children = [Node(board, node, first_win) for board, first_win in zip(children_boards, children_wins)]

            # backpropagation
            while node.parent is not None:
                node.games += len(possible_moves)
                node.wins += sum(children_wins)
                node = node.parent

