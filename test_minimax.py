import unittest
from agents.minimax_agent import MinimaxAgent
from main import Connect4

class TestMinimax(unittest.TestCase):
    def setUp(self):
        """set up test environmet"""
        self.agent = MinimaxAgent('○')
        self.empty = self.agent.empty_slot
    def test_choose_center_first(self):
        """test if agent makes a valid move on an empty board
            the most preferred position at te start is the centre columns, this test ensures the agent
            chooses centre col at the start
        """
        board = [[self.empty] * 7 for _ in range(6)] # get move
        move = self.agent.make_move(board)  # assert
        self.assertIn(move, range(7), "Move should be within valid column range")

    def test_block_opponent_win(self):
        """ test if agent immediately blocks an opponents win
             in the board below the opponents wins in one move,
             check the agent identifies this anf blocks it
        """
        board = [
            ['-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-'],
            ['●', '●', '●', '-', '-', '-', '-'],
        ]
        move = self.agent.make_move(board)
        self.assertEqual(move, 3, "Agent should block opponent's winning move")

    def test_go_for_win(self):
        """ check the agrnt identifies its own winning move"""
        board = [
            ['-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-'],
            ['○', '○', '○', '-', '-', '-', '-'],
        ]
        move = self.agent.make_move(board)
        self.assertEqual(move, 3, "Agent should win by completing 4-in-a-row")


if __name__ == '__main__':
    unittest.main()
