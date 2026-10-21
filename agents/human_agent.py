class HumanAgent:
    def __init__(self, symbol):
        self.symbol = symbol
    def make_move(self, board):
        """mechanism of making a move for human, modularised for efficiency"""
        while True:
            try:
                column = int(input("Choose a column (0-6): "))
                if 0 <= column < len(board[0]) and board[0][column] == '-':
                    return column
                print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter a number between 0-6.")
