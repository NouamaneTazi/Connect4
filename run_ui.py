import argparse
from Projets.puissance4.Nouamane_TAZI_Marah_GAMDOU import AIPlayer as AI1
from _MCTS import AIPlayer as AI2
from player import HumanPlayer, RandomPlayer
from alphabeta import AlphabetaPlayer
# from test import AIPlayer as AI3
from ui_game import UIGame


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--p1', default='Player1')
    parser.add_argument('--p2', default='Player2')
    args = parser.parse_args()

    # player1 = AI2()
    # player1 = HumanPlayer()
    player1 = AlphabetaPlayer(plays_first=True)
    player1.name = args.p1
    # player2 = HumanPlayer()
    # player2 = AlphabetaPlayer(plays_first=False)
    player2=AI2()
    player2.name = args.p2

    game = UIGame(player1, player2)
