###########################################################
# simple bot
###########################################################
import random
import pygame
class Bot:
    def __init__(self):
        self.possible_directions = ["LEFT", "RIGHT", "UP", "DOWN"]

    def choose_direction(self, player):
        # Évitez de faire demi-tour immédiatement
        if len(player.segments) > 1:
            self.possible_directions.remove(self.opposite_direction(player.direction))

        # Choisir une direction aléatoire parmi les directions possibles
        new_direction = random.choice(self.possible_directions)
        player.direction = new_direction
        return new_direction

    def opposite_direction(self, direction):
        if direction == "LEFT":
            return "RIGHT"
        elif direction == "RIGHT":
            return "LEFT"
        elif direction == "UP":
            return "DOWN"
        elif direction == "DOWN":
            return "UP"
        else:
            return None