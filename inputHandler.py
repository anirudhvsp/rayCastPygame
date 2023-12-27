import pygame
from constants import MOUSE_SENS, PLAYER_SPEED, ROTATION_SPEED, SPRINT_SPEED
from renderUtils import is_collision
import random
import math

class InputHandler:

    def __init__(self):
        self.sprinting = False

    def handle_input(self, game_state):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move_forward(game_state)
        if keys[pygame.K_s]:
            self.move_backward(game_state)
        if keys[pygame.K_a]:
            self.strafe_left(game_state)
        if keys[pygame.K_d]:
            self.strafe_right(game_state)
        if keys[pygame.K_RIGHT]:
            self.rotate_right(game_state)
        if keys[pygame.K_LEFT]:
            self.rotate_left(game_state)
        if keys[pygame.K_LSHIFT]:
            self.sprinting = True
        else:
            self.sprinting = False
        dx, dy = pygame.mouse.get_rel()
        dx *= MOUSE_SENS
        dy *= MOUSE_SENS
        self.rotate_mouse(game_state, dx, dy)

            
    def move_forward(self, game_state):
        if(self.sprinting):
            next_x = game_state.player_pos[0] +  SPRINT_SPEED * game_state.player_dir[0]
            next_y = game_state.player_pos[1] +  SPRINT_SPEED * game_state.player_dir[1]
        else:
            next_x = game_state.player_pos[0] +  PLAYER_SPEED * game_state.player_dir[0]
            next_y = game_state.player_pos[1] +  PLAYER_SPEED * game_state.player_dir[1]
        if not is_collision(next_x, next_y, game_state):
            game_state.player_pos[0] = next_x
            game_state.player_pos[1] = next_y


    def move_backward(self, game_state):
        next_x = game_state.player_pos[0] - PLAYER_SPEED * game_state.player_dir[0]
        next_y = game_state.player_pos[1] - PLAYER_SPEED * game_state.player_dir[1]
        if not is_collision(next_x, next_y, game_state):
            game_state.player_pos[0] = next_x
            game_state.player_pos[1] = next_y

    def strafe_left(self, game_state):
        next_x = game_state.player_pos[0] - PLAYER_SPEED * game_state.player_plane[0]
        next_y = game_state.player_pos[1] - PLAYER_SPEED * game_state.player_plane[1]
        if not is_collision(next_x, next_y, game_state):
            game_state.player_pos[0] = next_x
            game_state.player_pos[1] = next_y

    def strafe_right(self, game_state):
        next_x = game_state.player_pos[0] + PLAYER_SPEED * game_state.player_plane[0]
        next_y = game_state.player_pos[1] + PLAYER_SPEED * game_state.player_plane[1]
        if not is_collision(next_x, next_y, game_state):
            game_state.player_pos[0] = next_x
            game_state.player_pos[1] = next_y

    def rotate_right(self, game_state):
        game_state.player_dir = [
            game_state.player_dir[0] * math.cos(ROTATION_SPEED) - game_state.player_dir[1] * math.sin(ROTATION_SPEED),
            game_state.player_dir[0] * math.sin(ROTATION_SPEED) + game_state.player_dir[1] * math.cos(ROTATION_SPEED),
        ]
        game_state.player_plane = [
            game_state.player_plane[0] * math.cos(ROTATION_SPEED) - game_state.player_plane[1] * math.sin(ROTATION_SPEED),
            game_state.player_plane[0] * math.sin(ROTATION_SPEED) + game_state.player_plane[1] * math.cos(ROTATION_SPEED),
        ]

    def rotate_left(self, game_state):
        game_state.player_dir = [
            game_state.player_dir[0] * math.cos(-ROTATION_SPEED) - game_state.player_dir[1] * math.sin(-ROTATION_SPEED),
            game_state.player_dir[0] * math.sin(-ROTATION_SPEED) + game_state.player_dir[1] * math.cos(-ROTATION_SPEED),
        ]
        game_state.player_plane = [
            game_state.player_plane[0] * math.cos(-ROTATION_SPEED) - game_state.player_plane[1] * math.sin(-ROTATION_SPEED),
            game_state.player_plane[0] * math.sin(-ROTATION_SPEED) + game_state.player_plane[1] * math.cos(-ROTATION_SPEED),
        ]

    def rotate_mouse(self, game_state, dx, dy):
        game_state.player_dir = [
            game_state.player_dir[0] * math.cos(-dx) - game_state.player_dir[1] * math.sin(-dx),
            game_state.player_dir[0] * math.sin(-dx) + game_state.player_dir[1] * math.cos(-dx),
        ]

        game_state.player_plane = [
            game_state.player_plane[0] * math.cos(-dx) - game_state.player_plane[1] * math.sin(-dx),
            game_state.player_plane[0] * math.sin(-dx) + game_state.player_plane[1] * math.cos(-dx),
        ]

