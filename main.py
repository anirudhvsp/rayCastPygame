import pygame
import math
from renderUtils import draw_walls, draw_minimap, is_collision
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, ROTATION_SPEED, MOUSE_SENS,  BLACK, WHITE
from gameState import GameState
from inputHandler import InputHandler

# Initialize Pygame
pygame.init()


# Pygame setup
clock = pygame.time.Clock()

game_state = GameState()

def main():
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

        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, WHITE)
        
        # Adjust the position to the top right corner
        fps_position = (SCREEN_WIDTH - fps_text.get_width() - 10, 10)
        
        game_state.screen.blit(fps_text, fps_position)


        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
