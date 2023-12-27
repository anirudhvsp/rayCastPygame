import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class GameState:
    def __init__(self):
        self.player_pos = [2.5, 2.5]
        self.player_dir = [1, 0]
        self.player_plane = [0, 0.66]
        self.game_map = []
        self.camera_shake = 0.0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        with open("roomLayout.txt", "r") as file:
            room_layout = [list(line.strip()) for line in file]

        # Convert room layout to integers
        self.game_map = [[int(cell) for cell in row] for row in room_layout]