###########################################################
# bot with q_learning
###########################################################

import random
import csv
import os
import numpy as np
class Bot:
    def __init__(self, actions, epsilon=0.1, learning_rate=0.2, gamma=0.8, grid_size=10):
        self.q_table = self.load_q_table("q_table.csv")
        self.actions = actions
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.grid_size = grid_size  # Taille d'une case du jeu
        self.reward = 0
        # Charger les données après avoir défini load_data
        data = self.load_data("game_data.csv")  
        self.iteration_count = data["iteration_count"]
        self.total_reward = data["total_reward"]
        
    def getQ(self, state, action):
        """Get Q value for a state-action pair."""
        return self.q_table.get((state, action), 0.0)

    def get_state(self, snake, apple):
        snake_head_x, snake_head_y = snake.segments[0]["x"], snake.segments[0]["y"]
        apple_x, apple_y = apple.apple_position_x, apple.apple_position_y

        state = []

        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                # Ignorer la case où se trouve la tête
                if x_offset == 0 and y_offset == 0:
                    continue

                check_x = snake_head_x + x_offset * self.grid_size
                check_y = snake_head_y + y_offset * self.grid_size

                # Vérifier les collisions avec les murs et le corps
                state.append(1 if self.is_obstacle(check_x, check_y, snake) else 0)

        state.append(1 if apple_x < snake_head_x else 0)
        state.append(1 if apple_x > snake_head_x else 0)
        state.append(1 if apple_y < snake_head_y else 0)
        state.append(1 if apple_y > snake_head_y else 0)
        

        return tuple(state)

    def is_obstacle(self, x, y, snake):
        # Vérifie si les coordonnées sont hors limites ou sur le corps du serpent
        if (x < self.grid_size or x >= 600 - self.grid_size or 
            y < self.grid_size or y >= 400 - self.grid_size or
            {"x": x, "y": y} in snake.segments):
            return 1
        return 0

    def learnQ(self, state, action, reward, value):
        oldv = self.q_table.get((state, action), None)
        if oldv is None:
            self.q_table[(state, action)] = reward
        else:
            self.q_table[(state, action)] = oldv + self.learning_rate * (value - oldv)

    def update_q(self, state, action, reward, next_state):
        maxqnew = max([self.getQ(next_state, a) for a in self.actions])

        # Learn the Q-Value based on current reward and future
        # expected rewards.
        self.learnQ(state, action, reward, reward + self.gamma * maxqnew)

    def choose_action(self, state):
        """Epsilon-Greedy approach for action selection."""
        if random.random() < self.epsilon:
            # With probability epsilon, we select a random action
            action = random.choice(self.actions)
        else:
            # With probability 1-epsilon, we select the action
            # with the highest Q-value
            q = [self.getQ(state, a) for a in self.actions]
            maxQ = max(q)
            count = q.count(maxQ)
            # If there are multiple actions with the same Q-Value,
            # then choose randomly among them
            if count > 1:
                best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)

            action = self.actions[i]
        return action
    
    def save_q_table(self, filename="q_table.csv"):
        """Enregistrer la q_table dans un fichier CSV."""
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for (state, action), value in self.q_table.items():
                writer.writerow([str(state), action, value])
    def load_q_table(self, filename="q_table.csv"):
        """Charger la q_table depuis un fichier CSV."""
        q_table = {}
        if os.path.exists(filename):
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    state = eval(row[0])  # Convertir le texte en tuple
                    action = row[1]
                    value = float(row[2])
                    q_table[(state, action)] = value
        return q_table
    
    def save_data(self, filename="game_data.csv"):
        """Sauvegarde la q_table, la récompense totale et le nombre d'itérations."""
        data = {
            "iteration_count": self.iteration_count,
            "total_reward": self.total_reward
        }
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in data.items():
                writer.writerow([key, value])
        self.save_q_table("q_table.csv")

    def load_data(self, filename="game_data.csv"):
        """Charge les données du jeu depuis un fichier CSV."""
        data = {
            "iteration_count": 0,
            "total_reward": 0
        }
        if os.path.exists(filename):
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    key = row[0]
                    if key == "iteration_count":
                        data[key] = int(row[1])
                    elif key == "total_reward":
                        data[key] = float(row[1])
        return data