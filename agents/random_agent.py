import random

class RandomAgent:
    def __init__(self, symbol):
        self.symbol = symbol
    def make_move(self, board):
        """makes a random move from valid possible moves"""
        valid_moves = [col for col in range(len(board[0])) if board[0][col] == '-']
        return random.choice(valid_moves)
