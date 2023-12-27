import pygame
import math
from renderUtils import draw_walls, draw_minimap, is_collision
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, ROTATION_SPEED, MOUSE_SENS,  BLACK, WHITE
from gameState import GameState
from inputHandler import InputHandler
import asyncio

# Initialize Pygame
pygame.init()


# Pygame setup
clock = pygame.time.Clock()

game_state = GameState()

async def main():
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    font = pygame.font.Font(None, 15)

    input_handler = InputHandler()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        input_handler.handle_input(game_state)

        # Clear the screen
        game_state.screen.fill(BLACK)

        # Draw walls
        draw_walls(game_state)
        draw_minimap(game_state)


        # Update the display
        pygame.display.update()
        await asyncio.sleep(0)  # Very important, and keep it 0

        if not running:
            return

asyncio.run( main() )