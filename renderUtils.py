import pygame
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, ROTATION_SPEED, MOUSE_SENS, FOV,WHITE, BLACK, RED, GREY


def cast_ray(ray_angle, game_state):
    # Cast a ray and find the intersection point with walls
    ray_dir = [math.cos(ray_angle), math.sin(ray_angle)]

    # Check if ray_dir[1] is close to zero to avoid division by zero
    if abs(ray_dir[1]) < 1e-10:
        ray_dir[1] = 1e-10  # Set a small value to avoid division by zero

    map_pos = [int(game_state.player_pos[0]), int(game_state.player_pos[1])]

    # Calculate step and initial side distances
    delta_dist_x = abs(1 / ray_dir[0])
    delta_dist_y = abs(1 / ray_dir[1])

    if ray_dir[0] < 0:
        step_x = -1
        side_dist_x = (game_state.player_pos[0] - map_pos[0]) * delta_dist_x
    else:
        step_x = 1
        side_dist_x = (map_pos[0] + 1.0 - game_state.player_pos[0]) * delta_dist_x

    if ray_dir[1] < 0:
        step_y = -1
        side_dist_y = (game_state.player_pos[1] - map_pos[1]) * delta_dist_y
    else:
        step_y = 1
        side_dist_y = (map_pos[1] + 1.0 - game_state.player_pos[1]) * delta_dist_y

    # DDA algorithm
    while True:
        # Jump to the next map square
        if side_dist_x < side_dist_y:
            side_dist_x += delta_dist_x
            map_pos[0] += step_x
            side = 0  # Hit a vertical wall
        else:
            side_dist_y += delta_dist_y
            map_pos[1] += step_y
            side = 1  # Hit a horizontal wall

        # Check if the ray hits a wall
        if game_state.game_map[map_pos[1]][map_pos[0]] == 1:
            break

    # Calculate distance to the wall
    if side == 0:
        perp_wall_dist = (map_pos[0] - game_state.player_pos[0] + (1 - step_x) / 2) / ray_dir[0]
    else:
        perp_wall_dist = (map_pos[1] - game_state.player_pos[1] + (1 - step_y) / 2) / ray_dir[1]

    # Calculate wall height on game_state.screen
    line_height = int(SCREEN_HEIGHT / perp_wall_dist)

    return line_height, side


def draw_walls(game_state):
    for x in range(SCREEN_WIDTH):
        # Calculate ray angle for each column
        camera_x = 2 * x / SCREEN_WIDTH - 1  # Normalize x-coordinate
        ray_dir_x = game_state.player_dir[0] + game_state.player_plane[0] * camera_x
        ray_dir_y = game_state.player_dir[1] + game_state.player_plane[1] * camera_x

        # Angle of the ray with respect to player direction
        ray_angle = math.atan2(ray_dir_y, ray_dir_x)
        if ray_angle < 0:
            ray_angle += 2 * math.pi

        # Cast the ray
        line_height, side = cast_ray(ray_angle, game_state)

        # Calculate wall color based on the side of the wall
        wall_color = RED if side == 0 else WHITE
        floor_color = GREY
        # Draw the wall segment
        wall_start = (x, SCREEN_HEIGHT // 2 - line_height // 2)
        wall_end = (x, SCREEN_HEIGHT // 2 + line_height // 2)
        pygame.draw.line(game_state.screen, wall_color, wall_start, wall_end, 1)

        floor_start = (x, SCREEN_HEIGHT // 2 + line_height // 2)
        floor_end = (x, SCREEN_HEIGHT)
        pygame.draw.line(game_state.screen, floor_color, floor_start, floor_end)



def draw_minimap(game_state):
    # Draw the 2D representation of the game map
    for y, row in enumerate(game_state.game_map):
        for x, cell in enumerate(row):
            color = WHITE if cell == 1 else BLACK
            pygame.draw.rect(game_state.screen, color, (x * 10, y * 10, 10, 10))

    # Draw the player's position and direction on the minimap
    pygame.draw.circle(game_state.screen, RED, (int(game_state.player_pos[0] * 10), int(game_state.player_pos[1] * 10)), 3)
    player_end_x = int(game_state.player_pos[0] * 10 + 5 * game_state.player_dir[0])
    player_end_y = int(game_state.player_pos[1] * 10 + 5 * game_state.player_dir[1])
    pygame.draw.line(game_state.screen, RED, (int(game_state.player_pos[0] * 10), int(game_state.player_pos[1] * 10)), (player_end_x, player_end_y), 1)


def is_collision(x, y, game_state):
    # Check if the player's next position collides with a wall or goes out of bounds
    map_x = int(x)
    map_y = int(y)
    return game_state.game_map[map_y][map_x] == 1 or map_x < 0 or map_x >= len(game_state.game_map[0]) or map_y < 0 or map_y >= len(game_state.game_map)