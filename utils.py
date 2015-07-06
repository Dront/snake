import pygame
from params import params


def draw_grid(screen):
    tile_size = params['TILE_SIZE']
    win_size = params['WIN_SIZE']
    color = params['GRID_COLOR']

    for x in range(0, win_size[0], tile_size):
        pygame.draw.aaline(screen, color, (x, 0), (x, win_size[1]))

    for y in range(0, win_size[1], tile_size):
        pygame.draw.aaline(screen, color, (0, y), (win_size[0], y))