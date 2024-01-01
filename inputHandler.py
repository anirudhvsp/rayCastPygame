import pygame
from constants import *
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
        if keys[pygame.K_UP]:
            self.lookUp(game_state)
        if keys[pygame.K_DOWN]:
            self.lookDown(game_state)
        if keys[pygame.K_q]:
            self.increaseRenderQuality(game_state)
        if keys[pygame.K_e]:
            self.decreaseRenderQuality(game_state)

        
        dx, dy = pygame.mouse.get_rel()
        dx *= MOUSE_SENS
        dy *= MOUSE_SENS * 500
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
        # Rotate based on the x movement
        game_state.player_dir = [
            game_state.player_dir[0] * math.cos(-dx) - game_state.player_dir[1] * math.sin(-dx),
            game_state.player_dir[0] * math.sin(-dx) + game_state.player_dir[1] * math.cos(-dx),
        ]

        game_state.player_plane = [
            game_state.player_plane[0] * math.cos(-dx) - game_state.player_plane[1] * math.sin(-dx),
            game_state.player_plane[0] * math.sin(-dx) + game_state.player_plane[1] * math.cos(-dx),
        ]

        # Look up and down based on the y movement
        game_state.viewOffset += dy
        game_state.viewOffset = max(-VERTICAL_CLAMP, min(VERTICAL_CLAMP, game_state.viewOffset))  # Clamp between -60.0 and 60.0
    
    def lookUp(self, game_state):
        game_state.viewOffset += 1
        game_state.viewOffset = min(VERTICAL_CLAMP, game_state.viewOffset)  # Clamp to 60.0
    
    def lookDown(self, game_state):
        game_state.viewOffset -= 1
        game_state.viewOffset = max(-VERTICAL_CLAMP, game_state.viewOffset)  # Clamp to -60.0

    def increaseRenderQuality(self, game_state):
        game_state.RENDER_QUALITY += 0.1
        game_state.RENDER_QUALITY = min(64, game_state.RENDER_QUALITY)
    def decreaseRenderQuality(self, game_state):
        game_state.RENDER_QUALITY -= 0.1
        game_state.RENDER_QUALITY = max(1, game_state.RENDER_QUALITY)