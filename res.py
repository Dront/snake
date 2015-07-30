import os

from params import params
import pygame

tile_size = params['TILE_SIZE']

wall_pic = pygame.image.load(os.path.join(params['PIC_FOLDER'], params['WALL_PIC']))
wall_pic = pygame.transform.scale(wall_pic, (tile_size, tile_size)).convert()

ground_pic = pygame.image.load(os.path.join(params['PIC_FOLDER'], params['GROUND_PIC']))
ground_pic = pygame.transform.scale(ground_pic, (tile_size, tile_size)).convert()

icon = pygame.image.load(os.path.join(params['PIC_FOLDER'], params['ICON'])).convert_alpha()

snake_body_pic = pygame.image.load(os.path.join(params['PIC_FOLDER'], params['SNAKE_BODY_PIC']))
snake_body_pic = pygame.transform.scale(snake_body_pic, (tile_size, tile_size)).convert_alpha()

snake_head_pic = pygame.image.load(os.path.join(params['PIC_FOLDER'], params['SNAKE_HEAD_PIC']))
snake_head_pic = pygame.transform.scale(snake_head_pic, (tile_size, tile_size)).convert_alpha()

pygame.font.init()

small_font = pygame.font.Font(params['FONT'], 25)
small_font.set_bold(True)

big_font = pygame.font.Font(params['FONT'], 70)
big_font.set_bold(True)

res = {
    'WALL_PIC': wall_pic,
    'GROUND_PIC': ground_pic,
    'SNAKE_BODY_PIC': snake_body_pic,
    'SNAKE_HEAD_PIC': snake_head_pic,
    'ICON': icon,
    'BIG_FONT': big_font,
    'SMALL_FONT': small_font
}
