import numpy as np
import joblib
import random
import os

class MLAgent:
    def __init__(self, symbol, model_path=None):
        self.symbol = symbol
        self.opponent_symbol = '●' if symbol == '○' else '○'
        self.empty_slot = '-'
        self.columns = 7

        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'policy_network_model.joblib')

        self.model = joblib.load(model_path) # load model

    def board_to_arr(self, board):
        """converts 2d board o a 1d array input"""
        mapping = {self.symbol: 1, self.opponent_symbol: -1, self.empty_slot: 0}
        flat_board = [mapping[cell] for row in board for cell in row]

        return np.array(flat_board) # shape (42,)

    def get_valid_move(self, board):
        """ identifies col that are not full yet"""
        return [col for col in range(self.columns) if board[0][col] == self.empty_slot]

    def make_move(self, board):
        """chooses a move based on nn prediction"""
        if self.model is None:
            return self.random_valid_move(board)

        valid_moves = self.get_valid_move(board)
        if not valid_moves:
            return 0 # hopefully not

        input_array = self.board_to_arr(board)
        input_arr_2d = input_array.reshape(1, -1)

        prediction = self.model.predict(input_arr_2d)[0]

        predicted_col = int(prediction) # in case it comes as a float

        if prediction in valid_moves:
            return prediction
        else:
            return self.random_valid_move(board)

    def random_valid_move(self, board):
        """ fallback """
        valid_moves = self.get_valid_move(board)
        return random.choice(valid_moves)




"""
class MLAgent:
    def __init__(self, symbol, max_depth=5, top_k=3):
        self.symbol = symbol
        self.opponent_symbol = '●' if symbol == '○' else '○'
        self.model = joblib.load("agents/value_network.joblib")
        self.max_depth = max_depth
        self.top_k = top_k

    def make_move(self, board):
        best_move = None
        best_score = -float('inf')
        valid_moves = [col for col in range(7) if board[0][col] == '-']

        # check for immediate win
        for col in valid_moves:
            temp_board = self.simulate_move(board, col, self.opponent_symbol)
            if self.check_winner(temp_board) == self.symbol:
                return col

        # check for immediate blok
        for col in valid_moves:
            temp_board = self.simulate_move(board, col, self.opponent_symbol)
            if self.check_winner(temp_board) == self.opponent_symbol:
                return col

        # if neither, do minimax
        move_scores = []
        for col in valid_moves:
            temp_board = self.simulate_move(board, col, self.symbol)
            pred_score = self.evaluate_board(temp_board)
            move_scores.append((col, pred_score))

        move_scores.sort(key=lambda x: x[1], reverse=True)  # sort by best predicted score

        # 4. Explore only top_k moves
        top_moves = move_scores[:self.top_k]

        for col, _ in top_moves:
            temp_board = self.simulate_move(board, col, self.symbol)
            score = self.minimax(temp_board, self.max_depth - 1, False, -float('inf'), float('inf'))

            if score > best_score:
                best_score = score
                best_move = col

        return best_move if best_move is not None else self.random_valid_move(board)

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        winner = self.check_winner(board)
        if winner == self.symbol:
            return 1000
        elif winner == self.opponent_symbol:
            return -1000
        elif self.is_board_full(board):
            return 0

        if depth == 0:
            return self.evaluate_board(board)

        valid_col = [col for col in range(7) if board[0][col] == '-']

        if maximizing_player:
            max_eval = -float('inf')
            for col in valid_col:
                temp_board = self.simulate_move(board, col, self.symbol)
                eval = self.minimax(temp_board, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for col in valid_col:
                temp_board = self.simulate_move(board, col, self.opponent_symbol)
                eval = self.minimax(temp_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(alpha, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self, board):
        """"""uses ML model to predict outcome at leaf node""""""
        flat_board = []
        for row in board:
            for cell in row:
                if cell == self.symbol:
                    flat_board.append(1)
                elif cell == self.opponent_symbol:
                    flat_board.append(-1)
                else:
                    flat_board.append(0)
        input_arr = np.array(flat_board).reshape(1, -1)

        prediction = self.model.predict(input_arr)[0] # use model

        #add centre control score to boost
        column_weights = [1, 2, 4, 8, 4, 2, 1]
        center_score = 0
        for r in range(6):
            for c in range(7):
                if board[r][c] == self.symbol:
                    center_score += column_weights[c]
                elif board[r][c] == self.opponent_symbol:
                    center_score -= column_weights[c]  # Penalize opponent pieces

        return prediction * 1000 + center_score
    def simulate_move(self, board, col, symbol):
        """"""simulate playing""""""
        temp_board = [row.copy() for row in board]
        for row in range(5, -1, -1): # bottom row upwards
            if temp_board[row][col] == '-':
                temp_board[row][col] = symbol
                return temp_board
        return None

    def check_winner(self, board):
        """"""Check if there's a winner.""""""
        
        rows, cols = 6, 7
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == '-':
                    continue
                if c + 3 < cols and all(board[r][c + i] == board[r][c] for i in range(4)):
                    return board[r][c]
                if r + 3 < rows and all(board[r + i][c] == board[r][c] for i in range(4)):
                    return board[r][c]
                if r + 3 < rows and c + 3 < cols and all(board[r + i][c + i] == board[r][c] for i in range(4)):
                    return board[r][c]
                if r - 3 >= 0 and c + 3 < cols and all(board[r - i][c + i] == board[r][c] for i in range(4)):
                    return board[r][c]
        return None

    def is_board_full(self, board):
        """ """Check if the board is completely filled.
        return all(cell != '-' for cell in board[0])

    def random_valid_move(self, board):
        """ """fallback to random valid move""" """
        valid_cols = [col for col in range(7) if board[0][col] == '-']
        return random.choice(valid_cols) if valid_cols else 0

import numpy as np
import joblib
import random
from tensorflow.keras.models import load_model

class MLAgent:
    def __init__(self, symbol, model_type='cnn', model_path=None):
        '''model type is mlp or rf depending on which model is used'''
        self.symbol = symbol
        self.opponent_symbol = '●' if symbol == '○' else '○'
        self.model_type = model_type

        if not model_path:
            model_path = f"agents/ml_model_{model_type}.joblib" if model_type != 'cnn' else "agents/cnn_model.h5"

        if model_type == 'cnn':
            self.model = load_model(model_path)
        else:
            self.model = joblib.load(model_path)

    def make_move(self, board):
        # convert visual symbols to numerical dataset format: 'x', 'o', 'b'
        flat_board = []
        for row in board:
            for cell in row:
                if cell == self.symbol:
                    flat_board.append(1)
                elif cell == self.opponent_symbol:
                    flat_board.append(-1)
                else:
                    flat_board.append(0)

        if self.model_type == 'cnn':
            input_array = np.array(flat_board).reshape(1, 6, 7, 1)
            probs = self.model.predict(input_array)[0]  # softmax output
            sorted_cols = np.argsort(probs)[::-1]  # sort columns by predicted probability
        else:
            #append current_plaer as extra feature
            current_player_val = 1 if self.symbol == '●' else -1
            input_array = np.array(flat_board + [current_player_val]).reshape(1, -1)
            pred_col = self.model.predict(input_array)[0]
            sorted_cols = [pred_col]  # single prediction

        # Choose the best valid move
        for col in sorted_cols:
            if board[0][col] == '-':
                return col

        # fallback
        return self.random_valid_move(board)

    def random_valid_move(self, board):
        #fallback if no predicted outcome match is found
        valid_cols = [col for col in range(7) if board[0][col] == '-']
        return random.choice(valid_cols) if valid_cols else 0"""