import unittest
from agents.random_agent import RandomAgent
from main import Connect4

class TestRandom(unittest.TestCase):
    def setUp(self):
        """ set up environmentt"""
        self.agent = RandomAgent('○')
        self.empty_board = [[Connect4.empty_slot] * Connect4.columns for _ in range(Connect4.rows)]

    def test_returns_valid_move(self): # check it returns a valid col
        """ test that it returns a valid col in the board"""
        move = self.agent.make_move(self.empty_board)
        self.assertIn(move, range(Connect4.columns))

    def test_avoids_full_columns(self): # check it returns non full col
        """ check tht it doesnt choose a col thats alr full"""
        full_board = [row[:] for row in self.empty_board]
        for row in full_board:
            row[3] = '●'  # Fill up column 3
        moves = [self.agent.make_move(full_board) for _ in range(20)]
        self.assertNotIn(3, moves)

if __name__ == '__main__':
    unittest.main()
