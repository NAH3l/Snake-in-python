###########################################################
# bot with q_learning
###########################################################

import random

class Bot:
    def __init__(self, actions, epsilon=0.1, learning_rate=0.2, gamma=0.9, grid_size=10):
        self.q_table = {}
        self.actions = actions  
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.grid_size = grid_size  # Taille d'une case du jeu
        self.reward = -1
        
    def getQ(self, state, action):
        """Get Q value for a state-action pair."""
        return self.q_table.get((state, action), 0.0)

    def get_state(self, snake, apple):
        snake_head_x, snake_head_y = snake.segments[0]["x"], snake.segments[0]["y"]
        apple_x, apple_y = apple.apple_position_x, apple.apple_position_y

        state = []

        # Vérifier les obstacles dans un rayon de 2 cases
        for x_offset in range(-2, 3):
            for y_offset in range(-2, 3):
                # Ignorer la case où se trouve la tête
                if x_offset == 0 and y_offset == 0:
                    continue

                check_x = snake_head_x + x_offset * self.grid_size
                check_y = snake_head_y + y_offset * self.grid_size

                # Vérifier les collisions avec les murs et le corps
                state.append(self.is_obstacle(check_x, check_y, snake))

        # Informations sur la pomme 
        state.append(apple_x < snake_head_x)
        state.append(apple_x > snake_head_x)
        state.append(apple_y < snake_head_y)
        state.append(apple_y > snake_head_y)

        return tuple(state)

    def is_obstacle(self, x, y, snake):
        # Vérifie si les coordonnées sont hors limites ou sur le corps du serpent
        if (x < self.grid_size or x >= 600 - self.grid_size or 
            y < self.grid_size or y >= 400 - self.grid_size or
            {"x": x, "y": y} in snake.segments):
            return True
        return False

    def update_q(self, state, action, reward, next_state):
        """Update Q value for a state-action pair."""
        current_q = self.q_table.get((state, action), 0.0)
        best_next_q = max([self.getQ(next_state, a) for a in self.actions], default=0)
        self.q_table[(state, action)] = current_q + self.learning_rate * (reward + self.gamma * best_next_q - current_q)

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