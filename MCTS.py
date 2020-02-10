from numpy import sqrt, log, argmax
from alphabeta import AlphabetaPlayer
from copy import deepcopy
from random import choice
from board import Board
import time

class Node: # an explored board
    def __init__(self, board=Board(), parent=None, first_win=0, games=0, depth=0):
        self.board = board
        self.children = [] # [Nodes]
        self.parent = parent # Node
        self.wins = first_win
        self.games = games
        self.depth = depth
        self.c = sqrt(2)

    def get_uct(self):
        if self.games == 0:
            return None
        return (self.wins / self.games) + self.c * sqrt( log(self.parent.games) / self.games)

    def get_cor_player(self): # Returns corresponding player for node's children
        return (-1)**self.depth

class Agent: #Suppose im player 1
    def __init__(self):
        pass

    def simulate(self, board, player): # returns 1 if player wins
        plays_first = (player==-1) # Decides of p1 token || player = p2
        p1 = AlphabetaPlayer(max_level=2, plays_first=plays_first, heuristic=False)
        p2 = AlphabetaPlayer(max_level=2, plays_first=not plays_first, heuristic=False)
        while True:
            # print(board)
            p1_move = p1.getColumn(board) # p1 plays first
            if p1_move != None:
                row = board.play(p1.my_id, p1_move)
                if p1.getWinner(board, (p1_move,row)):
                    return 0 # p1 WINS
            else: return 1 # p2 WINS
            p2_move = p2.getColumn(board)
            if p2_move != None:
                row = board.play(p2.my_id, p2_move)
                if p1.getWinner(board, (p2_move,row)):
                    return 1 # p2 WINS
            else: return 0 # p1 WINS

    def train_mcts_once(self, root_node):
        # SELECTION
        node = root_node
        while len(node.children) > 0:
            ucts = [child.get_uct() for child in node.children]
            if None in ucts:
                node = choice(node.children)
            else:
                # print(["%.2f"%i for i in ucts])
                node = node.children[argmax(ucts)]
            # node = node.children[0]

        # EXPANSION
        possible_moves = node.board.getPossibleColumns()
        if len(possible_moves) > 0: # not a terminal node
            player = node.get_cor_player()

            # Make move
            children_boards = [deepcopy(node.board) for _ in range(len(possible_moves))]
            [children_boards[i].play(player, possible_moves[i]) for i in range(len(possible_moves))]

            # SIMULATION
            children_wins = [int(self.simulate(deepcopy(child_board), player))
                             for child_board in children_boards] #[1,0,1,0,..]
            node.children = [Node(board, node, first_win, 1, node.depth+1)
                             for board, first_win in zip(children_boards, children_wins)]

            # BACKPROPAGATION
            wins = sum(children_wins)
            losses = len(children_wins) - wins
            node.games += len(possible_moves)
            node.wins += losses
            flag = True
            while node.parent != None:
                node = node.parent
                node.games += len(possible_moves)
                node.wins += wins if flag else losses
                flag = not flag
        # print([(child.wins, child.games) for child in node.children])
        # print()
        return node

    def train_mcts_ntimes(self, root_node, n):
        node = root_node
        for _ in range(n):
            self.train_mcts_once(node)
        move, k = -1, 0
        while True: #5000 -> 6
            try:
                print("Player "+str((-1)**k)+", make a choice :" )
                print("Lvl: %d | Move: %d | Node: %d/%d"%(node.depth, move, node.wins, node.games))
                print(["%d/%d"%(child.wins, child.games) for child in node.children])
                print()
                move = argmax([child.wins for child in node.children])
                node=node.children[move]
                k+=1
            except:
                break

t0 = time.time()
Agent().train_mcts_ntimes(Node(),100)
print(time.time() - t0)

# 4 : 4.9
# 20 : 1.8
# 100 : 9.7
