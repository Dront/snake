import pygame
from params import params


def constrain(x, left, right):
        if x < left:
            return left
        if x > right:
            return right
        return x


class Tile(object):
    """
    Represents one tile from the grid
    """

    def __init__(self, coords, color):
        self.color = color
        self.coords = coords
        self.rect = pygame.Rect(self.coords, (params['TILE_SIZE'], params['TILE_SIZE']))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Snake(object):
    """
    Represents player
    """

    tile = params['TILE_SIZE']
    UP = (0, -tile)
    DOWN = (0, tile)
    LEFT = (-tile, 0)
    RIGHT = (tile, 0)

    def __init__(self):
        self.head = Tile(params['START_POS'], params['HEAD_COLOR'])
        self.dir = self.UP

    def go(self):
        # TODO
        # move tail first

        tmp = self.head.coords
        x = tmp[0] + self.dir[0]
        y = tmp[1] + self.dir[1]

        x = constrain(x, 0, params['WIN_SIZE'][0])
        y = constrain(y, 0, params['WIN_SIZE'][1])

        self.head = Tile((x, y), params['HEAD_COLOR'])

    def change_dir(self, dir):
        if dir == 'UP':
            self.dir = self.UP
        elif dir == 'DOWN':
            self.dir = self.DOWN
        elif dir == 'LEFT':
            self.dir = self.LEFT
        elif dir == 'RIGHT':
            self.dir = self.RIGHT

    def draw(self, screen):
        self.head.draw(screen)