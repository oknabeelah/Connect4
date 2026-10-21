import random

class RuleBasedAgent:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, board):
        """check for a win to make, a possible block or fallback on random"""
        valid_moves = [col for col in range(len(board[0])) if board[0][col] == '-']

        # Winning move
        for col in valid_moves:
            temp_board = [row[:] for row in board]
            for row in reversed(temp_board):
                if row[col] == '-':
                    row[col] = self.symbol
                    break
            if self.is_winner(temp_board, self.symbol):
                return col

        # Blocking move
        opponent_symbol = '●' if self.symbol == '○' else '○'
        for col in valid_moves:
            temp_board = [row[:] for row in board]
            for row in reversed(temp_board):
                if row[col] == '-':
                    row[col] = opponent_symbol
                    break
            if self.is_winner(temp_board, opponent_symbol):
                return col

        # Random move as fallback
        return random.choice(valid_moves)

    @staticmethod
    def is_winner(board, symbol):
        """adding another is_winner method for code modularity"""
        rows = len(board)
        cols = len(board[0])

        # Horizontal Check
        for row in range(rows):
            for col in range(cols - 3):
                if all(board[row][col + i] == symbol for i in range(4)):
                    return True

        # Vertical Check
        for row in range(rows - 3):
            for col in range(cols):
                if all(board[row + i][col] == symbol for i in range(4)):
                    return True

        # Diagonal (Bottom Left to Top Right)
        for row in range(3, rows):
            for col in range(cols - 3):
                if all(board[row - i][col + i] == symbol for i in range(4)):
                    return True

        # Diagonal (Top Left to Bottom Right)
        for row in range(rows - 3):
            for col in range(cols - 3):
                if all(board[row + i][col + i] == symbol for i in range(4)):
                    return True

        return False