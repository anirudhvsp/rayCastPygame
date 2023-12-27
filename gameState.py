import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
import roomLayout
class GameState:
    def __init__(self):
        self.player_pos = [2.5, 2.5]
        self.player_dir = [1, 0]
        self.player_plane = [0, 0.66]
        self.game_map = []
        self.camera_shake = 0.0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Convert room layout to integers
        self.game_map = roomLayout.ROOM1