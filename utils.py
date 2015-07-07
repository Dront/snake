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


def draw_text(screen, text):
    font = pygame.font.SysFont('Sans', 25)
    rendered_text = font.render(text, True, params['TEXT_COLOR'])
    center_x = (params['WIN_SIZE'][0] // 2) - (rendered_text.get_width() // 2)
    center_y = (params['WIN_SIZE'][1] // 2) - (rendered_text.get_height() // 2)
    screen.blit(rendered_text, [center_x, center_y])


def draw_score(screen, score):
    font = pygame.font.SysFont('Sans', 25)
    text = font.render('Score: ' + str(score), True, params['SCORE_COLOR'])
    x = (params['WIN_SIZE'][0] // 2) - (text.get_width() // 2)
    y = text.get_height() // 2
    screen.blit(text, [x, y])


def check_for_collisions(tile, obstacles):
    """
    :param tile: single tile
    :param obstacles: list of tiles
    :return: True if tile collides with obstacles, False otherwise
    """
    [x, y] = tile.coords

    for obs in obstacles:
        if x == obs.coords[0] and y == obs.coords[1]:
            return True

    return False