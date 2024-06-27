import pygame
import random

class Apple:
    def __init__(self, screen, rect_x, rect_y, rect_width, rect_height):
        self.screen = screen
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.border_color = (255, 0, 0)
        self.rect_size = 10
        self.apple_position_x, self.apple_position_y = self.random_position()

    # Random apple coordinates  
    def random_position(self):
        self.apple_x = random.randint(self.rect_x, self.rect_x + self.rect_width - self.rect_size)
        self.apple_y = random.randint(self.rect_y, self.rect_y + self.rect_height - self.rect_size)
        
        self.apple_x = (self.apple_x // self.rect_size) * self.rect_size
        self.apple_y = (self.apple_y // self.rect_size) * self.rect_size
        return self.apple_x, self.apple_y

    # Update apple position
    def update_position(self):
        self.apple_position_x, self.apple_position_y = self.random_position()

    # Apple display
    def draw_apple(self):
        apple_radius = self.rect_size // 2  # Calculating radius of the circle
        apple_center = (self.apple_position_x + apple_radius, self.apple_position_y + apple_radius)  # Center of the circle
        pygame.draw.circle(self.screen, self.border_color, apple_center, apple_radius)


class SnakePlayer:
    def __init__(self, screen, rect_x, rect_y, rect_width, rect_height):
        self.screen = screen
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.border_color = (0, 128, 0)
        self.rect_size = 10
        self.player_position_x, self.player_position_y = self.random_position_init() 
        self.segments = [{
            "x": self.player_position_x, # x coordonate of a segment 
            "y": self.player_position_y  # y coordonate of a segment
        }]
        self.direction = None  # Initial direction None to stand still
        self.score = 0
        self.speed = 10

    # Random coordinates of the first segment at the start of a game
    def random_position_init(self):
        self.player_x = random.randint(self.rect_x, self.rect_x + self.rect_width - self.rect_size)
        self.player_y = random.randint(self.rect_y, self.rect_y + self.rect_height - self.rect_size)
        
        self.player_x = (self.player_x // self.rect_size) * self.rect_size
        self.player_y = (self.player_y // self.rect_size) * self.rect_size
        return self.player_x, self.player_y

    # Display the player
    def draw_player(self):
        for segment in self.segments:
            pygame.draw.rect(self.screen, self.border_color, pygame.Rect(segment["x"], segment["y"], self.rect_size, self.rect_size))
    
    # Handle the keys
    
    def handle_keys(self):
        keys = pygame.key.get_pressed()
        new_direction = self.direction

        if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and self.direction != "RIGHT":
            new_direction = "LEFT"
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_f]) and self.direction != "LEFT":
            new_direction = "RIGHT"
        elif (keys[pygame.K_UP] or keys[pygame.K_z]) and self.direction != "DOWN":
            new_direction = "UP"
        elif (keys[pygame.K_DOWN] or keys[pygame.K_e]) and self.direction != "UP":
            new_direction = "DOWN"

        if new_direction != self.direction:
            self.direction = new_direction

    # Move the player
    def move_player(self):
        if self.direction is None:
            return
        
        # Move segments from back to front
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i]["x"] = self.segments[i - 1]["x"]
            self.segments[i]["y"] = self.segments[i - 1]["y"]

        # Move the head segment
        if self.direction == "LEFT":
            self.segments[0]["x"] -= self.rect_size
        elif self.direction == "RIGHT":
            self.segments[0]["x"] += self.rect_size
        elif self.direction == "UP":
            self.segments[0]["y"] -= self.rect_size
        elif self.direction == "DOWN":
            self.segments[0]["y"] += self.rect_size

    # Add a new segment to the player
    def grow(self):
        last_segment = self.segments[-1]
        new_segment = {
            "x": last_segment["x"],
            "y": last_segment["y"]
        }
        self.segments.append(new_segment)