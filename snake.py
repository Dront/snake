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
    UP = [0, -tile]
    DOWN = [0, tile]
    LEFT = [-tile, 0]
    RIGHT = [tile, 0]

    def __init__(self):
        self.cur_dir = self.UP
        self.head = Tile(params['START_POS'], params['HEAD_COLOR'])
        self.size = params['START_SIZE']
        self.next_dir = None

        self.body = []
        pos = self.head.coords
        for i in range(1, self.size):
            pos = [pos[0] - self.cur_dir[0], pos[1] - self.cur_dir[1]]
            self.body.append(Tile(pos, params['BODY_COLOR']))

    def go(self):

        if self.next_dir is not None:
            self.cur_dir = self.next_dir
            self.next_dir = None

        tmp = list(self.head.coords)

        new_tile = Tile(tmp, params['BODY_COLOR'])
        self.body.insert(0, new_tile)
        self.body.pop()

        tmp = [tmp[0] + self.cur_dir[0], tmp[1] + self.cur_dir[1]]

        self.head = Tile(tmp, params['HEAD_COLOR'])

    def change_dir(self, dir):
        if dir == 'UP':
            if self.cur_dir != self.DOWN:
                self.next_dir = self.UP
        elif dir == 'DOWN':
            if self.cur_dir != self.UP:
                self.next_dir = self.DOWN
        elif dir == 'LEFT':
            if self.cur_dir != self.RIGHT:
                self.next_dir = self.LEFT
        elif dir == 'RIGHT':
            if self.cur_dir != self.LEFT:
                self.next_dir = self.RIGHT

    def draw(self, screen):
        for tile in self.body:
            tile.draw(screen)
        self.head.draw(screen)