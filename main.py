import pygame
import random
from entities import SnakePlayer, Apple
from rules import Jeu
import affichage

# Exemple d'utilisation
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Snake Game")

    rect_width, rect_height = 500, 300
    rect_size = 10
    rect_x = ((600 - rect_width) // 2) // rect_size * rect_size  # Position x multiple de 10
    rect_y = ((400 - rect_height) // 2) // rect_size * rect_size  # Position y multiple de 10
    rect_width = (rect_width // rect_size) * rect_size
    rect_height = (rect_height // rect_size) * rect_size

    jeu = Jeu(screen, rect_x, rect_y, rect_width, rect_height)  # Créer l'instance de Jeu ici
    jeu.run_game()

    