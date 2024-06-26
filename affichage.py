import pygame
import random
from entities import SnakePlayer, Apple
import csv

def initialistion(jeu):
    # Ouvrir le fichier CSV en mode écriture
    with open("game_info.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Écrire l'en-tête du fichier CSV
        writer.writerow(["Segment", "X", "Y"])

        # Écrire les positions des segments du serpent
        for i, segment in enumerate(jeu.player.segments):
            writer.writerow([f"Segment {i+1}", segment["x"], segment["y"]])

        # Écrire la position de la pomme
        writer.writerow(["Pomme", jeu.apple.apple_position_x, jeu.apple.apple_position_y])

        # Écrire la direction du serpent
        writer.writerow(["Direction", jeu.player.direction])

def forward_propagation(file):
    