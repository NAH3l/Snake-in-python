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

    def getQ(self, state, action):
        """Get Q value for a state-action pair."""
        return self.q_table.get((state, action), 0.0)

    def get_state(self, snake, apple):
        snake_head_x, snake_head_y = snake.segments[0]["x"], snake.segments[0]["y"]
        apple_x, apple_y = apple.apple_position_x, apple.apple_position_y

        # Check if there is an obstacle
        state = [
            (snake_head_x > self.grid_size and ({"x": snake_head_x - self.grid_size, "y": snake_head_y} in snake.segments)),
            (snake_head_x < 600 - 2 * self.grid_size and ({"x": snake_head_x + self.grid_size, "y": snake_head_y} in snake.segments)),
            (snake_head_y > self.grid_size and ({"x": snake_head_x, "y": snake_head_y - self.grid_size} in snake.segments)),
            (snake_head_y < 400 - 2 * self.grid_size and ({"x": snake_head_x, "y": snake_head_y + self.grid_size} in snake.segments)),
            (snake_head_x > self.grid_size and snake_head_y > self.grid_size and ({"x": snake_head_x - self.grid_size, "y": snake_head_y - self.grid_size} in snake.segments)),
            (snake_head_x < 600 - 2 * self.grid_size and snake_head_y > self.grid_size and ({"x": snake_head_x + self.grid_size, "y": snake_head_y - self.grid_size} in snake.segments)),
            (snake_head_x > self.grid_size and snake_head_y < 400 - 2 * self.grid_size and ({"x": snake_head_x - self.grid_size, "y": snake_head_y + self.grid_size} in snake.segments)),
            (snake_head_x < 600 - 2 * self.grid_size and snake_head_y < 400 - 2 * self.grid_size and ({"x": snake_head_x + self.grid_size, "y": snake_head_y + self.grid_size} in snake.segments)),
            (apple_x < snake_head_x),
            (apple_x > snake_head_x),
            (apple_y < snake_head_y),
            (apple_y > snake_head_y), 
            (snake.is_body_ahead("UP")),
            (snake.is_body_ahead("DOWN")),
            (snake.is_body_ahead("LEFT")),
            (snake.is_body_ahead("RIGHT")),
        ]
        return tuple(state)

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