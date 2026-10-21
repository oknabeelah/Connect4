import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime

class AnalyticsLogger:
    def __init__(self, agent1, agent2):
        self.agent1 = agent1.__class__.__name__ if not isinstance(agent1, str) else agent1.replace(" ", "")
        self.agent2 = agent2.__class__.__name__ if not isinstance(agent2, str) else agent2.replace(" ", "")
        self.start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.folder = f"analytics_logs/{self.agent1}_vs_{self.agent2}_{self.start_time}"
        os.makedirs(self.folder, exist_ok=True)

        self.records = []
        self.metrics = {
            self.agent1: {"wins": 0, "draws": 0, "losses": 0, "total_nodes": 0, "total_time": 0.0, "total_prunes": 0},
            self.agent2: {"wins": 0, "draws": 0, "losses": 0, "total_nodes": 0, "total_time": 0.0, "total_prunes": 0}
        }

    def log_game(self, game_index, winner, agent_data=None):
        record = {
            "Game": game_index,
            "Winner": winner or "Draw"
        }

        print("Returned winner:", winner)
        print("Logger expects:", self.agent1, self.agent2)

        # update tallies
        if winner == self.agent1:
            self.metrics[self.agent1]["wins"] += 1
            self.metrics[self.agent2]["losses"] += 1
        elif winner == self.agent2:
            self.metrics[self.agent2]["wins"] += 1
            self.metrics[self.agent1]["losses"] += 1
        else:
            self.metrics[self.agent1]["draws"] += 1
            self.metrics[self.agent2]["draws"] += 1 # ish here

        # add additional data (nodes, time, pruning) if provided
        if agent_data:
            for agent, data in agent_data.items():
                self.metrics[agent]["total_nodes"] += data.get("nodes", 0)
                self.metrics[agent]["total_time"] += data.get("time", 0.0)
                self.metrics[agent]["total_prunes"] += data.get("prunes", 0)

        self.records.append(record)

    def export_csv(self):
        game_log_path = os.path.join(self.folder, "game_results.csv")
        with open(game_log_path, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Game", "Winner"])
            writer.writeheader()
            writer.writerows(self.records)

        summary_path = os.path.join(self.folder, "summary.csv")
        with open(summary_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Agent", "Wins", "Draws", "Losses", "Avg Nodes", "Avg Time", "Total Prunes"])
            for agent, data in self.metrics.items():
                n_games = len(self.records) #self.metrics[self.agent1]["wins"] + self.metrics[self.agent2]["wins"] + self.metrics[self.agent1]["draws"]
                writer.writerow([
                    agent,
                    data["wins"],
                    data["draws"],
                    data["losses"],
                    round(data["total_nodes"] / max(n_games, 1), 2),
                    round(data["total_time"] / max(n_games, 1), 4),
                    data["total_prunes"]
                ])

    def export_bar_chart(self): # ?
        labels = ["Wins", "Draws", "Losses"]
        agent1_vals = [self.metrics[self.agent1]["wins"], self.metrics[self.agent1]["draws"], self.metrics[self.agent1]["losses"]]
        agent2_vals = [self.metrics[self.agent2]["wins"], self.metrics[self.agent2]["draws"], self.metrics[self.agent2]["losses"]]

        x = range(len(labels))
        plt.figure(figsize=(8, 5))
        plt.bar([i - 0.2 for i in x], agent1_vals, width=0.4, label=self.agent1)
        plt.bar([i + 0.2 for i in x], agent2_vals, width=0.4, label=self.agent2)
        plt.xticks(x, labels)
        plt.ylabel("Number of Games")
        plt.title("Performance Comparison")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.folder, "performance_summary.png"))
        plt.close()
