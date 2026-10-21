import pandas as pd
import numpy as np
from unlzw3 import unlzw
from tqdm import tqdm

"""reprocess dataset to show board states and next move to win: with features as board state in 1d and label as outcome and move pair"""
def row_to_board(row):
    return np.array(row[:42]).reshape(6, 7)

def board_to_numeric(board):
    mapping = {'x': 1, 'o': -1, 'b': 0}
    return np.vectorize(mapping.get)(board)

def simulate_game_moves(row, outcome):
    board = row_to_board(row)
    symbols = row[:42]
    sequence = [s for s in symbols if s != 'b']
    results = []

    moves_made = 0
    current_board = np.full((6, 7), 'b')
    for move_index in range(len(sequence)):
        col = None
        move_symbol = sequence[move_index]
        for c in range(7):
            col_height = np.count_nonzero(current_board[:, c] != 'b')
            if col_height < 6 and board[5 - col_height][c] == move_symbol:
                col = c
                break
        if col is None:
            continue
        for r in reversed(range(6)):
            if current_board[r][col] == 'b':
                current_board[r][col] = move_symbol
                break
        moves_made += 1
        if moves_made >= 2 and move_index + 1 < len(sequence):
            current_player = sequence[move_index + 1]
            numeric_board = board_to_numeric(current_board)
            next_col = None
            for c in range(7):
                col_height = np.count_nonzero(current_board[:, c] != 'b')
                if col_height < 6 and board[5 - col_height][c] == current_player:
                    next_col = c
                    break
            if next_col is not None:
                results.append((numeric_board.flatten(), current_player, next_col))
    return results

with open("connect-4.data.Z", 'rb') as f:
    decompressed = unlzw(f.read())
with open("connect-4.csv", 'wb') as f:
    f.write(decompressed)

column_names = [f"cell_{i}" for i in range(42)] + ["outcome"]
data = pd.read_csv("connect-4.csv", names=column_names)
data = data[data['outcome'].isin(['win', 'draw'])] # exclude loss to train better

X_data = []
y_data = []

for _, row in tqdm(data.iterrows(), total=len(data)):
    row_data = row.values[:-1]
    outcome = row['outcome']
    examples = simulate_game_moves(row_data, outcome)
    for board_flat, player, col in examples:
        X_data.append(board_flat)
        y_data.append((1 if player == 'x' else -1, col))

X = np.array(X_data)
y = np.array(y_data)

np.save("X_progressive.npy", X)
np.save("y_progressive.npy", y)
print(f"Saved {X.shape[0]} samples: shape {X.shape}, labels shape {y.shape}")
