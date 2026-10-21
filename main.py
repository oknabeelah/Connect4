from agents.human_agent import HumanAgent
from agents.random_agent import RandomAgent
from agents.rule_based_agent import RuleBasedAgent
from agents.minimax_agent import MinimaxAgent
from agents.ml_agent import MLAgent
from analytics_logger import AnalyticsLogger

class Connect4:
    """has game setup/layout, play game and run simulation methods """
    rows = 6
    columns = 7
    empty_slot = '-'

    def __init__(self, agent1, agent2):
        #initialise board
        self.board = [[self.empty_slot for _ in range(self.columns)] for _ in range(self.rows)]

        # assign symbol to agents
        self.players = {agent1: '●', agent2: '○'}
        self.current_player = agent1

        # initialise agents
        self.agent1 = self.create_agent(agent1, '●')
        self.agent2 = self.create_agent(agent2, '○')

    @staticmethod
    def create_agent(agent, symbol):
        """creates agent when prompted to access their class, adding a human agent for separation needed in run_simulation method"""
        if agent == 'Human':
            return HumanAgent(symbol)
        elif agent == 'Random Agent':
            return RandomAgent(symbol)
        elif agent == 'Rule-based Agent':
            return RuleBasedAgent(symbol)
        elif agent == 'Minimax Agent':
            return MinimaxAgent(symbol)
        elif agent == 'ML Agent':
            return MLAgent(symbol)
        return None
    def display_board(self):
        """prints board"""
        for row in self.board:
            print(' '.join(row))
        print('0 1 2 3 4 5 6')
        print()

    def is_valid_move(self, column):
        """checks if a move is valid"""
        return 0 <= column < self.columns and self.board[0][column] == self.empty_slot

    def make_move(self, column):
        """checks a move is made"""
        if self.is_valid_move(column):
            for row in reversed(self.board):
                if row[column] == self.empty_slot:
                    row[column] = self.players[self.current_player]
                    return True
        return False

    def switch_player(self):
        """switch player to continue gameplay"""
        self.current_player = list(self.players.keys())[0] if self.current_player == list(self.players.keys())[1] else list(self.players.keys())[1]
    @staticmethod
    def is_winner_static(board, symbol):  # static methods dotn take self signature
        """checks if the game is won"""
        # Horizontal Check
        for row in range(Connect4.rows):  # iterates through each row
            for col in range(
                    Connect4.columns - 3):  # for each row, check every possible starting col where 4 cons discs can fit
                if all(board[row][col + i] == symbol for i in
                       range(4)):  # check if all 4 cons slots contain same disc symbol
                    return True

        # Vertical Check
        for row in range(Connect4.rows - 3):
            for col in range(Connect4.columns):  # for each col, check every poss starting row where 4 cons disc can fit
                if all(board[row + i][col] == symbol for i in range(4)):
                    return True

        # Diagonal (Bottom Left to Top Right)
        for row in range(3, Connect4.rows):  # starts from row 4 and goes to the last row
            for col in range(Connect4.columns - 3):  # for each starting point, checks 4 cons slots ina diag pattent
                if all(board[row - i][col + i] == symbol for i in range(4)):
                    return True

        # Diagonal (Top Left to Bottom Right)
        for row in range(Connect4.rows - 3):  # starts from row 1 to 3rd to last
            for col in range(Connect4.columns - 3):
                if all(board[row + i][col + i] == symbol for i in range(4)):
                    return True
        return False

    def is_draw(self):
        """check if there's a draw"""
        return all(self.board[0][col] != self.empty_slot for col in range(self.columns))

    def play(self):
        """method that controls the game"""
        # check both agents are initialized before starting
        if self.agent1 is None or self.agent2 is None:
            print("Both agents must be initialized.")
            return "Error"

        # game loop
        while True:
            # display board
            self.display_board()

            # choose the current agent
            current_agent = self.agent1 if self.current_player == list(self.players.keys())[0] else self.agent2
            column = current_agent.make_move(self.board)

            # make the move and check for a win or draw
            if self.make_move(column):
                if Connect4.is_winner_static(self.board, self.players[self.current_player]):
                    self.display_board()
                    print(f'{self.current_player} wins!')
                    ############# generate game tree at the end
                    if isinstance(self.agent1, MinimaxAgent):
                        folder = f"{type(self.agent1).__name__} vs {type(self.agent2).__name__}"
                        self.agent1.export_all_trees(folder)
                    elif isinstance(self.agent2, MinimaxAgent):
                        folder = f"{type(self.agent1).__name__} vs {type(self.agent2).__name__}"
                        self.agent2.export_all_trees(folder)
                    ############
                    #return self.current_player
                    if self.current_player == list(self.players.keys())[0]:
                        return self.agent1.__class__.__name__
                    else:
                        return self.agent2.__class__.__name__
                if self.is_draw():
                    self.display_board()
                    print('Draw!')
                    #####
                    if isinstance(self.agent1, MinimaxAgent):
                        folder = f"{type(self.agent1).__name__} vs {type(self.agent2).__name__}"
                        self.agent1.export_all_trees(folder)
                    elif isinstance(self.agent2, MinimaxAgent):
                        folder = f"{type(self.agent1).__name__} vs {type(self.agent2).__name__}"
                        self.agent2.export_all_trees(folder)
                    #####
                    return 'Draw'
                # switch player
                self.switch_player()
            else:
                print(f"Invalid move by {self.current_player}. Trying again...")

    @staticmethod
    def run_sim():
        """used to test ai agents against each other"""
        print("Select two AI agents to compete:")
        print("1. Random Agent")
        print("2. Rule Based Agent")
        print("3. Minimax Agent")
        print("4. ML Agent")
        agent_choices = {1: 'Random Agent', 2: 'Rule-based Agent', 3: 'Minimax Agent', 4: 'ML Agent'}
        # get ageent names
        agent1_name = agent_choices.get(int(input('Select AI agent 1 (1-4): ')), 'Random Agent')
        agent2_name = agent_choices.get(int(input('Select AI agent 2 (1-4): ')), 'Random Agent')

        logger = AnalyticsLogger(
            agent1_name, agent2_name
            #test_agent1.__class__.__name__,
            #test_agent2.__class__.__name__
        )
        game_num = 0 # initialise

        agent1_wins = 0
        agent2_wins = 0
        draws = 0

        for _ in range(500): #CHANGE BACK TO 500 lollol
            game = Connect4(agent1_name, agent2_name)

            if isinstance(game.agent1, MinimaxAgent):
                game.agent1.visualize = False
            if isinstance(game.agent2, MinimaxAgent):
                game.agent2.visualize = False

            test_agent1 = game.agent1
            test_agent2 = game.agent2

            game_num += 1 # set counter
            result = game.play()

            if result == agent1_name:
                agent1_wins += 1
            elif result == agent2_name:
                agent2_wins += 1
            else:
                draws += 1

            agent_data = {}

            for agent in [test_agent1, test_agent2]:
                name = agent.__class__.__name__
                metrics = {}
                if hasattr(agent, "nodes_evaluated"):
                    metrics["nodes"] = getattr(agent, "nodes_evaluated", 0)
                if hasattr(agent, "total_time"):
                    metrics["time"] = getattr(agent, "total_time", 0.0)
                if hasattr(agent, "pruned_branches"):  # meep moop
                    metrics["prunes"] = getattr(agent, "pruned_branches", 0)
                if metrics:
                    agent_data[name] = metrics

            logger.log_game(game_num, result, agent_data)

            print(f'{agent1_name} wins: {agent1_wins}')
            print(f'{agent2_name} wins: {agent2_wins}')
            print(f'draws: {draws}')

        logger.export_csv()
        logger.export_bar_chart()

if __name__ == '__main__':
    print('1. Human vs AI')
    print('2. AI vs AI')
    mode = int(input('Enter mode to play (1-2): '))
    if mode == 1:
        print('Select your opponent')
        print('1: Random Agent')
        print('2: Rule-based Agent')
        print('3: Minimax Agent')
        print('4: ML Agent')
        choice = int(input('Enter your choice (1-4): '))
        opponents = {1: 'Random Agent', 2: 'Rule-based Agent', 3: 'Minimax Agent', 4: 'ML Agent'}
        opponent = opponents.get(choice, 'Random Agent')  # if user chooses an invalid option ie default
        game = Connect4('Human', opponent)
        game.play()
    elif mode == 2:
        Connect4.run_sim()

