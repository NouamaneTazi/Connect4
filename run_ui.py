import argparse

from player import HumanPlayer, RandomPlayer
from TEST import AIPlayer
# from test import AIPlayer as AI3
from ui_game import UIGame


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--p1', default='AI')
    parser.add_argument('--p2', default='adv')
    args = parser.parse_args()

    player1 = HumanPlayer()
    # player1 = AIPlayer()
    # player1.p1_id, player1.p2_id = player1.p2_id, player1.p1_id
    player1.name = args.p1
    # player2 = HumanPlayer()
    player2 = AIPlayer()
    player2.name = args.p2

    game = UIGame(player1, player2)
