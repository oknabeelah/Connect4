import unittest
from agents.rule_based_agent import RuleBasedAgent
from main import Connect4

class TestRuleBasedAgent(unittest.TestCase):
    def setUp(self):
        """ sety upo test environt"""
        self.agent = RuleBasedAgent('○')
        self.empty_board = [[Connect4.empty_slot] * Connect4.columns for _ in range(Connect4.rows)]

    def drop_piece(self, board, col, symbol): # force winning move
        """ helper method to simulate dropping a piece into a clo, finds lowest availabel row in a col specified and places symbol there"""
        for row in reversed(board):
            if row[col] == Connect4.empty_slot:
                row[col] = symbol
                break

    def test_winning_move(self):
        """ test if the agent prioritieses winnimg moves"""
        board = [row[:] for row in self.empty_board]
        for _ in range(3):
            self.drop_piece(board, 0, '○') # simulate a scene wit three o's in a col and check
            # agent drops a disc in that col
        self.assertEqual(self.agent.make_move(board), 0)

    def test_block_opponent(self):
        """ test if agent prioritises blocking opps move"""
        board = [row[:] for row in self.empty_board]
        for _ in range(3): # simulates above scene
            self.drop_piece(board, 1, '●')
        self.assertEqual(self.agent.make_move(board), 1)  #  opp also drops a disc in the next col, check that agent blocks this


if __name__ == '__main__':
    unittest.main()
