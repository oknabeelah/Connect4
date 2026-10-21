import unittest
import numpy as np
import os
import random
from agents.ml_agent import MLAgent
from main import Connect4

class TestMLAgentSimple(unittest.TestCase):
    """test suite for MLAgent using a dummy model."""

    prediction = 2 # column the dummy model always predicts. edit: 3 doesnt work ;(
    model_path = os.path.join('agents', 'dummy_policy_model.joblib')

    @classmethod
    def setUpClass(cls):
        """ check if the dummy model file exists before running tests."""
        if not os.path.exists(cls.model_path):
            raise FileNotFoundError(
                f"Dummy model file not found at '{cls.model_path}'. "
                f"Please run create_dummy_model.py first."
            )

    def setUp(self):
        """ set up for tests"""
        self.symbol = '○'
        self.opponent_symbol = '●'
        self.empty_slot = Connect4.empty_slot
        self.rows = Connect4.rows
        self.columns = Connect4.columns
        self.empty_board = [[self.empty_slot] * self.columns for _ in range(self.rows)]
        # create an agent instance for tests
        try:
            self.agent = MLAgent(self.symbol)
        except Exception as e:
            self.fail(f"Failed to initialize MLAgent, likely model loading issue: {e}")

    def test_initialization(self):
        """ test basic agent attributes after initialization."""
        self.assertEqual(self.agent.symbol, self.symbol)
        self.assertEqual(self.agent.opponent_symbol, self.opponent_symbol)
        self.assertEqual(self.agent.columns, self.columns)
        # Check if the model was loaded (is not None)
        self.assertIsNotNone(self.agent.model, "Model should be loaded from dummy file.")

    def test_board_to_arr_conversion(self):
        """ test the conversion of a board to the flat array format."""
        board = [
            [self.empty_slot] * self.columns,
            [self.empty_slot] * self.columns,
            [self.empty_slot] * self.columns,
            [self.empty_slot] * self.columns,
            [self.empty_slot, self.empty_slot, self.opponent_symbol, self.empty_slot, self.empty_slot, self.empty_slot, self.empty_slot],
            [self.empty_slot, self.symbol, self.opponent_symbol, self.symbol, self.empty_slot, self.empty_slot, self.empty_slot],
        ]
        expected_len = self.rows * self.columns
        expected_array_part = [0, 1, -1, 1, 0, 0, 0] # corresponds to the last row

        flat_array = self.agent.board_to_arr(board)

        self.assertIsInstance(flat_array, np.ndarray, "Should return a numpy array.")
        self.assertEqual(len(flat_array), expected_len, f"Array length should be {expected_len}.")
        # check some vals: 1 for self, -1 for opponent, 0 for empty
        self.assertEqual(flat_array[36], 1)
        self.assertEqual(flat_array[37], -1)
        self.assertEqual(flat_array[38], 1)
        self.assertEqual(flat_array[39], 0)

        self.assertTrue(np.array_equal(flat_array[-self.columns:], expected_array_part))

    def test_get_valid_moves(self):
        """ test identification of valid, non-full columns."""
        # test on empty board
        self.assertListEqual(self.agent.get_valid_move(self.empty_board), list(range(self.columns)))

        # test on partially full board
        board = [row[:] for row in self.empty_board]
        board[0][2] = self.symbol # make col 2 look full at the top
        board[0][5] = self.opponent_symbol # make col 5 look full at the top
        expected_valid = [0, 1, 3, 4, 6]
        self.assertListEqual(self.agent.get_valid_move(board), expected_valid)

        # test on completely full board (top row)
        full_top_board = [row[:] for row in self.empty_board]
        full_top_board[0] = [self.symbol] * self.columns
        self.assertListEqual(self.agent.get_valid_move(full_top_board), [])

    def test_make_move_on_empty_board_uses_dummy_model(self):
        """ test make_move returns the dummy model's prediction on an empty board."""
        move = self.agent.make_move(self.empty_board)
        # check if move is predicted by dummy model
        self.assertEqual(move, self.prediction)
        # double check it's a valid col
        self.assertIn(move, range(self.columns))

    def test_make_move_falls_back_if_dummy_prediction_invalid(self):
        """ test agent falls back to random if dummy model predicts a full column."""
        # create a board where the dummy's predicted col (3) is full
        board = [row[:] for row in self.empty_board]
        for r in range(self.rows):
            board[r][self.prediction] = self.opponent_symbol # fill col 3

        move = self.agent.make_move(board)

        self.assertNotEqual(move, self.prediction, "Should not return the full column.")
        valid_alternatives = [0, 1, 2, 4, 5, 6]
        self.assertIn(move, valid_alternatives, "Move must be a valid alternative column.")

    def test_make_move_full_board(self):
        """ test agent returns 0 if the board is completely full."""
        full_board = [[self.opponent_symbol] * self.columns for _ in range(self.rows)]
        move = self.agent.make_move(full_board)
        self.assertEqual(move, 0, "Should return 0 for a full board.")

    def test_random_fallback_if_model_set_to_none(self):
        """ test if agent uses random fallback when its model is None."""
        # manually disable the model for this test
        self.agent.model = None

        # seed random for predictable output
        random.seed(42)
        expected_random_choice = random.choice(list(range(self.columns)))
        random.seed(42) # reset seed for acc call

        move = self.agent.make_move(self.empty_board)

        # expect random choice among valid cols
        self.assertEqual(move, expected_random_choice)
        self.assertIn(move, range(self.columns))


if __name__ == '__main__':
    unittest.main()