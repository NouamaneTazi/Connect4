import numpy as np
from alphabeta import AlphabetaPlayer
from copy import deepcopy
import random
from board import Board

class Node: # an explored board
    def __init__(self, board=Board(), parent=None, first_win=0):
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
    def __init__(self):
        pass

    def simulate(self, board):
        p1 = AlphabetaPlayer(depth=2, plays_first=True)
        p2 = AlphabetaPlayer(depth=2, plays_first=False)
        while True:
            # try except return 0 ?
            p1_move = p1.getColumn(board)
            if p1_move: board.play(1, p1_move)
            else:
                print(board)
                return 0 # p2 WINS

            p2_move = p2.getColumn(board)
            if p2_move: board.play(-1, p2_move)
            else:
                print(board)
                return 1 # p1 WINS

    def train_mcts_once(self, root_node, player=1):
        # selection
        node = root_node
        while len(node.children) > 0:
            ucts = [child.get_uct() for child in node.children]
            if None in ucts:
                node = random.choice(node.children)
            else:
                node = node.children[np.argmax(ucts)]

        # expansion
        # print(node.board)
        possible_moves = node.board.getPossibleColumns()
        # print(len(possible_moves))
        if len(possible_moves) > 0: # not a terminal node
            children_boards = [deepcopy(node.board) for _ in range(len(possible_moves))]
            [children_boards[i].play(player, possible_moves[i]) for i in range(len(possible_moves))]
            # print(children_boards)
            # simulation
            children_wins = [self.simulate(deepcopy(board)) for board in children_boards] #[1,0,1,0,..]
            node.children = [Node(board, node, first_win) for board, first_win in zip(children_boards, children_wins)]

            # backpropagation
            while node.parent is not None:
                node.games += len(possible_moves)
                node.wins += sum(children_wins)
                node = node.parent

        print([(child.wins, child.games) for child in node.children])
        return node

    def train_mcts_ntimes(self, n):
        node = Node()
        for _ in range(n):
            self.train_mcts_once(node)

Agent().train_mcts_ntimes(2)
