import csv
import os
from agents.minimax_agent import MinimaxAgent
from main import Connect4

# directory
Dataset_file  = "minimax_data.csv"
num_games = 1000 # total games to simulate

def board_to_flat(board, symbol, opponent):
    """ flattens 2d connect 4 board to a 1d array"""
    mapping = {symbol: 1, opponent: -1, '-': 0}
    return [mapping[cell] for row in board for cell in row]

def generate_data():
    with open(Dataset_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['f' + str(i) for i in range(42)] + ['move'])  # 6x7 board + move column

        row_counter = 0

        for game_index in range(num_games):
            board = [['-' for _ in range(7)] for _ in range(6)]
            agent1 = MinimaxAgent('●', visualize=False)
            agent2 = MinimaxAgent('○', visualize=False)
            agents = {'●': agent1, '○': agent2}
            current_symbol = '●'
            moves = []

            while True:
                current_agent = agents[current_symbol]
                move = current_agent.make_move(board)
                moves.append((board_to_flat(board, current_symbol, '○' if current_symbol == '●' else '●'), move))

                # apply the move
                for row in reversed(board):
                    if row[move] == '-':
                        row[move] = current_symbol
                        break

                # check win/draw
                if Connect4.is_winner_static(board, current_symbol) or all(board[0][col] != '-' for col in range(7)):
                    break

                # switch player
                current_symbol = '○' if current_symbol == '●' else '●'

            for features, move in moves:
                writer.writerow(features + [move])
                row_counter += 1
                if row_counter % 100 == 0:
                    print(f"Written {row_counter} rows...")


if __name__ == "__main__":
    generate_data()