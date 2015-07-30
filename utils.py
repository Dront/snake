import pygame
from params import params
from res import res


def draw_grid(screen):
    tile_size = params['TILE_SIZE']
    win_size = params['WIN_SIZE']
    color = params['GRID_COLOR']

    for x in range(0, win_size[0], tile_size):
        pygame.draw.aaline(screen, color, (x, 0), (x, win_size[1]))

    for y in range(0, win_size[1], tile_size):
        pygame.draw.aaline(screen, color, (0, y), (win_size[0], y))


def draw_screen(screen, text):
    rendered_text = res['BIG_FONT'].render(text, True, params['TEXT_COLOR'])
    center_x = (params['WIN_SIZE'][0] // 2) - (rendered_text.get_width() // 2)
    center_y = (params['WIN_SIZE'][1] // 2) - (rendered_text.get_height() // 2)
    screen.blit(rendered_text, [center_x, center_y])
    pass


def draw_text(screen, text):
    rendered_text = res['SMALL_FONT'].render(text, True, params['TEXT_COLOR'])
    center_x = (params['WIN_SIZE'][0] // 2) - (rendered_text.get_width() // 2)
    center_y = (params['WIN_SIZE'][1] // 2) - (rendered_text.get_height() // 2)
    screen.blit(rendered_text, [center_x, center_y])


def draw_score(screen, score, high_score):
    small_font = res['SMALL_FONT']
    score_text = small_font.render('Score: ' + str(score), True, params['TEXT_COLOR'])
    high_score_text = small_font.render('Best: ' + str(high_score), True, params['TEXT_COLOR'])

    x = score_text.get_width()
    y = score_text.get_height()

    x = score_text.get_width() // 2
    y = score_text.get_height() // 2
    screen.blit(score_text, [x, y])

    x = params['WIN_SIZE'][0] - high_score_text.get_width() * 1.5
    y = high_score_text.get_height() // 2
    screen.blit(high_score_text, [x, y])


def constrain(x, left, right):
        if x < left:
            return left
        if x > right:
            return right
        return x
