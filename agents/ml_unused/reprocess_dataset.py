import pandas as pd
import numpy as np
from unlzw3 import unlzw
from tqdm import tqdm

# reprocess data set: extract last move and make a board vs last move pair input

# load and decompress
with open('connect-4.data.Z', 'rb') as f:
    decompressed = unlzw(f.read())
with open('connect-4.csv', 'wb') as f:
    f.write(decompressed)

# read data
cols = [f'cell_{i}' for i in range(42)] + ['outcome']
data = pd.read_csv('connect-4.csv', names=cols)

# filter to only include rows with outcome "win" or "draw"
filtered_data = data[data['outcome'].isin(['win', 'draw'])]
def row_to_grid(row):
    '''create 6x7 board from flat row'''
    return np.array(row[:42]).reshape((6, 7))
def find_last_move(board):
    '''find the last move made by 'x'''
    for row in reversed(range(6)):
        for col in range(7):
            if board[row][col] == 'x':
                return (row, col)
    return None
# build feature label pairs
X_boards = []
y_moves = []

for idx, row in tqdm(data.iterrows(), total=len(data)):
    board = row_to_grid(row)
    last_move = find_last_move(board)

    if last_move is None:
        continue  # skip if no move found

    row_idx, col_idx = last_move
    board_before = board.copy()
    board_before[row_idx][col_idx] = 'b'  # remove the move

    # convert symbols to numeric
    symbol_to_int = {'x': 1, 'o': -1, 'b': 0}
    board_before_num = np.vectorize(symbol_to_int.get)(board_before)

    X_boards.append(board_before_num.flatten())
    y_moves.append(col_idx)

# save into files for training
X = np.array(X_boards)
y = np.array(y_moves)

np.save('X_move_train.npy', X)
np.save('y_move_train.npy', y)

print(f"Saved {X.shape[0]} training samples for move prediction.")
