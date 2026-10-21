import random
import math
import copy
import datetime
import time
import os

class MinimaxAgent:
    '''minimax agent with alpha beta pruning'''
    def __init__(self, symbol, rows=6, columns=7, empty_slot='-', depth=4, visualize=True): # independent of connedct4 class, depth is how many moves ahead
        self.symbol = symbol # stores agent symbol
        self.opponent_symbol = '●' if self.symbol == '○' else '○'
        self.rows = rows
        self.columns = columns
        self.empty_slot = empty_slot
        self.depth = depth # store board dimension and depth for in class use
        self.saved_trees = []  # list to store (TreeNode, timestamp)
        self.visualize = visualize  # flag
        self.nodes_evaluated = 0
        self.pruned_branches = 0
        self.total_time = 0.0

    def make_move(self, board):
        '''implements minimax algorithm to decide next move'''
        self.nodes_evaluated = 0
        self.pruned_branches = 0
        self.total_time = 0.0
        start_time = time.time()
        best_score = -math.inf # start with worst possible score
        best_col = random.choice([col for col in range(self.columns) if board[0][col] == self.empty_slot]) # pick a random col as fallback

        self.root_node = TreeNode(board, depth=self.depth, maximizing=True)

        for col in range(self.columns):
            if board[0][col] == self.empty_slot:
                temp_board = copy.deepcopy(board)
                self.drop_piece(temp_board, col, self.symbol) #make simulated move,
                child_node = TreeNode(temp_board, move=col, depth=self.depth - 1, maximizing=False)
                self.root_node.add_child(child_node)
                score = self.minimax(temp_board, self.depth - 1, False, -math.inf, math.inf, child_node) #score using minimax
                if score > best_score:
                    best_score = score
                    best_col = col # track score and return best move based on scorw with

        self.total_time = time.time() - start_time

        if self.visualize:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")  # save timestamp and tree
            self.saved_trees.append((self.root_node, timestamp))
        return best_col

    def minimax(self, board, depth, maximizing_player, alpha, beta, node=None):#recursively simulate both player moves
        '''use alpha beta pruning efficiently facilitate the standard minimax algorithm'''
        valid_moves = [col for col in range(self.columns) if board[0][col] == self.empty_slot]

        self.nodes_evaluated += 1
        if depth == 0 or self.is_winner_static(board, self.symbol) or self.is_winner_static(board, self.opponent_symbol) or not valid_moves:
            score = self.evaluate_board(board) # maximise self and minimise opp for each level
            if node:
                node.score = score
            return score

        if maximizing_player:
            max_eval = -math.inf
            for col in valid_moves:
                temp_board = copy.deepcopy(board)
                self.drop_piece(temp_board, col, self.symbol)
                child_node = TreeNode(temp_board, move=col, depth=depth, maximizing=True)
                if node:
                    node.add_child(child_node)
                eval = self.minimax(temp_board, depth - 1, False, alpha, beta, child_node)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    self.pruned_branches += 1
                    break  # prune
            if node:
                node.score = max_eval
            return max_eval
        else:
            min_eval = math.inf
            for col in valid_moves:
                temp_board = copy.deepcopy(board)
                self.drop_piece(temp_board, col, self.opponent_symbol)
                child_node = TreeNode(temp_board, move=col, depth=depth, maximizing=False)
                if node:
                    node.add_child(child_node)
                eval = self.minimax(temp_board, depth - 1, True, alpha, beta, child_node)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    self.pruned_branches += 1
                    break  # prune
            if node:
                node.score = min_eval
            return min_eval

    def drop_piece(self, board, col, symbol): #place disc in lowest available row in a given col
        for row in reversed(board):
            if row[col] == self.empty_slot:
                row[col] = symbol
                break

    def evaluate_board(self, board): #asign score to col
        '''helper: intuitively evaluate the board and return a score'''
        score = 0
        center_col = [row[self.columns // 2] for row in board]
        score += center_col.count(self.symbol) * 3 #prefers center col

        score += self.count_windows(board, self.symbol, 4) * 1000 # more score for 4 in a row
        score += self.count_windows(board, self.symbol, 3) * 100 #
        score += self.count_windows(board, self.symbol, 2) * 10 #

        score -= self.count_windows(board, self.opponent_symbol, 4) * 1000 # penalise opp accordingluy
        score -= self.count_windows(board, self.opponent_symbol, 3) * 100
        score -= self.count_windows(board, self.opponent_symbol, 2) * 10
        return score

    def count_windows(self, board, symbol, num): # pattern recog, looks for hor, ver and diag windows of 4 cels
        '''helper'''
        count = 0 #estimate how close player is to winning
        # Horizontal
        for r in range(self.rows):
            for c in range(self.columns - 3):
                window = [board[r][c+i] for i in range(4)]
                if window.count(symbol) == num and window.count(self.empty_slot) == 4 - num:
                    count += 1
        # Vertical
        for c in range(self.columns):
            for r in range(self.rows - 3):
                window = [board[r+i][c] for i in range(4)]
                if window.count(symbol) == num and window.count(self.empty_slot) == 4 - num:
                    count += 1
        # Diagonal /
        for r in range(3, self.rows):
            for c in range(self.columns - 3):
                window = [board[r-i][c+i] for i in range(4)]
                if window.count(symbol) == num and window.count(self.empty_slot) == 4 - num:
                    count += 1
        # Diagonal \
        for r in range(self.rows - 3):
            for c in range(self.columns - 3):
                window = [board[r+i][c+i] for i in range(4)]
                if window.count(symbol) == num and window.count(self.empty_slot) == 4 - num:
                    count += 1
        return count

    def is_winner_static(self, board, symbol):
        '''using another is_winne rmethod becasue agent is independent of Connect4 class'''
        # Horizontal
        for r in range(self.rows):
            for c in range(self.columns - 3):
                if all(board[r][c+i] == symbol for i in range(4)):
                    return True
        # Vertical
        for c in range(self.columns):
            for r in range(self.rows - 3):
                if all(board[r+i][c] == symbol for i in range(4)):
                    return True
        # Diagonal /
        for r in range(3, self.rows):
            for c in range(self.columns - 3):
                if all(board[r-i][c+i] == symbol for i in range(4)):
                    return True
        # Diagonal \
        for r in range(self.rows - 3):
            for c in range(self.columns - 3):
                if all(board[r+i][c+i] == symbol for i in range(4)):
                    return True
        return False
    def export_all_trees(self, folder_name="trees"):
        os.makedirs(folder_name, exist_ok=True)
        for i, (tree, timestamp) in enumerate(self.saved_trees):
            filename = os.path.join(folder_name, f"minimax_tree_{timestamp}.svg") # changed from png to svg for clarity
            #filename = os.path.join(folder_name, f"minimax_tree_{timestamp}.png") # for if you want png
            tree.visualize(filename)
        print(f"Exported {len(self.saved_trees)} tree images to '{folder_name}'")

class TreeNode:
    '''tree data structure for each minimax decision'''
    def __init__(self, board, move=None, score=None, depth=0, maximizing=True):
        self.board = board
        self.move = move
        self.score = score
        self.depth = depth
        self.maximizing = maximizing
        self.children = []
    def add_child(self, child_node):
        self.children.append(child_node)
    def visualize(self, filename="minimax_tree.svg"): # change filename to minimax_tree.png
        '''uses libraries to visualise tree diagrams'''
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.DiGraph()
        node_labels = {}
        color_map = []

        def add_nodes_edges(node, parent_id=None, counter=[0]):
            node_id = counter[0]
            counter[0] += 1
            label = f"{node.move if node.move is not None else 'Root'}\n{node.score}"
            node_labels[node_id] = label
            color_map.append('skyblue' if node.maximizing else 'lightcoral')
            G.add_node(node_id)

            if parent_id is not None:
                G.add_edge(parent_id, node_id)

            for child in node.children:
                add_nodes_edges(child, node_id, counter)

        add_nodes_edges(self)

        # dynamic sizing based on number of nodes (to improve visibility of individual nodes
        node_count = len(G.nodes)
        depth_levels = max(node.depth for node in self.collect_nodes())
        width = max(12, node_count // 10)  # wider if many nodes
        height = max(6, depth_levels)  # taller if deeper tree

        pos = nx.nx_pydot.graphviz_layout(G, prog='dot')

        plt.figure(figsize=(width, height))
        nx.draw(G, pos, with_labels=False, arrows=True, node_size=2000, node_color=color_map)
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
        plt.title("Minimax Tree Visualization")
        plt.tight_layout()
        plt.savefig(filename, format='svg') # svg format
        #plt.savefig(filename, format='png') # for if you want a png fiel
        plt.close()
        return filename

    def collect_nodes(self):
        """helper to collect all nodes in tree, stalling tree generation to end of game for computational efficiency"""
        all_nodes = [self]
        for child in self.children:
            all_nodes.extend(child.collect_nodes())
        return all_nodes




