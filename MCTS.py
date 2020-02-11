from numpy import sqrt, log, argmax
from alphabeta import AlphabetaPlayer
from copy import deepcopy
from random import choice
from board import Board
import time

class Node: # an explored board
    def __init__(self, board=Board(), parent=None, first_win=0, is_terminal=False, games=0, depth=0):
        self.board = board
        self.children = [None]*7 # [Nodes]
        self.parent = parent # Node
        self.is_terminal = is_terminal
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

    def simulate(self, board, player, last_pos): # returns 1 if player wins
        # Decides of p1 token || player = p2
        p1 = AlphabetaPlayer(max_level=2, plays_first=(player==-1), heuristic=False) # plays_first here is just for token
        p2 = AlphabetaPlayer(max_level=2, plays_first=(player==1), heuristic=False)
        if p1.getWinner(board, last_pos):
            # print(player)
            # print(board)
            return 1, True
        while True:
            # print(board)
            p1_move = p1.getColumn(board) # p1 plays first
            if p1_move != None:
                row = board.play(p1.my_id, p1_move)
                if p1.getWinner(board, (p1_move,row)):
                    # print(board)
                    return 0, False # p1 WINS
            else: return 1, False # p2 WINS
            p2_move = p2.getColumn(board)
            if p2_move != None:
                row = board.play(p2.my_id, p2_move)
                if p1.getWinner(board, (p2_move,row)):
                    return 1, False # p2 WINS
            else:
                # print(board)
                return 0, False # p1 WINS

    def train_mcts_once(self, root_node):
        # SELECTION
        node = root_node
        while node.children != [None]*7:
            ucts = [child.get_uct() if child!=None else None for child in node.children]
            # print(["%.2f"%i for i in ucts])
            node = node.children[argmax(ucts)]
            # node = node.children[0]

        if node.is_terminal: #alrdy won
            print(node.get_cor_player())
            print(node.board)
            print("Node is terminal")
            # return None

        # EXPANSION
        possible_moves = node.board.getPossibleColumns()
        if len(possible_moves) == 0: # not a terminal node
            return None

        if node.is_terminal:
            wins = len(possible_moves) * 2 # TODO situation where we both almost win
            losses = len(possible_moves) - wins
            node.games += len(possible_moves)
            node.wins += wins
            flag = True
            while node.parent != None:
                node = node.parent
                node.games += len(possible_moves)
                node.wins += losses if flag else wins
                flag = not flag
        else:
            player = node.get_cor_player()

            # Make move
            children_boards = [deepcopy(node.board) for _ in range(len(possible_moves))]
            rows = [children_boards[i].play(player, possible_moves[i]) for i in range(len(possible_moves))]


            # SIMULATION
            children_wins = [self.simulate(deepcopy(child_board), player, (col,row)) # [(1,False),(0,False),(1,False),(0,False),..]
                             for child_board, col, row in zip(children_boards, possible_moves, rows)]

            for board, move, tuple in zip(children_boards, possible_moves, children_wins):
                node.children[move] = Node(board, node, tuple[0], tuple[1], 1, node.depth+1)

            # BACKPROPAGATION
            wins = sum([tuple[0] for tuple in children_wins])
            losses = len(possible_moves) - wins
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

    def train_mcts_ntimes(self, root_node, n, verbose=False):
        node = root_node
        k = node.depth
        for _ in range(n):
            self.train_mcts_once(node)
        if verbose:
            move = -1
            while True: #5000 -> 6
                try:
                    print("Player "+str((-1)**k)+", make a choice :" )
                    print("Lvl: %d | Move: %d | Node: %d/%d"%(node.depth, move, node.wins, node.games))
                    print(["%d/%d"%(child.wins, child.games) if child!=None else "None" for child in node.children ])
                    print()
                    move = argmax([child.wins for child in node.children])
                    node=node.children[move]
                    k+=1
                except:
                    break

if __name__ == '__main__':
    for _ in range(1):
        t0 = time.time()
        Agent().train_mcts_ntimes(Node(),100, verbose=True)
        print(time.time() - t0)

# 4 : 4.9
# 20 : 1.8
# 100 : 9.7
