import pygame
import random
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


class Obstacle(Tile):
    """
    Class represents obstacles on map. Convenience class.
    """

    def __init__(self, coords):
        Tile.__init__(self, coords, params['OBSTACLE_COLOR'])


class ObstacleContainer(object):
    """
    Represents all obstacle on map
    """

    def __init__(self, filename=None):

        # TODO
        # load map from file
        # at the moment, just hardcoded default map

        # import os
        # cur_path = os.getcwd()
        # map_path = os.path.join(cur_path, params['MAP_FOLDER'], filename)
        #
        # print map_path
        #
        # with open(map_path, 'r') as map_file:

        self.tiles = []

        if filename is None:
            tile = params['TILE_SIZE']
            tmp_y = params['WIN_SIZE'][1] - tile
            tmp_x = params['WIN_SIZE'][0] - tile

            for x in range(0, params['WIN_SIZE'][0], tile):
                self.tiles.append(Obstacle([x, 0]))
                self.tiles.append(Obstacle([x, tmp_y]))

            for y in range(tile, params['WIN_SIZE'][1] - tile, tile):
                self.tiles.append(Obstacle([0, y]))
                self.tiles.append(Obstacle([tmp_x, y]))

        else:
            raise NotImplementedError

    def draw(self, screen):
        for tile in self.tiles:
            tile.draw(screen)


class Fruit(Tile):
    """
    Class represents fruits for snake.
    """

    def __init__(self, coords):
        Tile.__init__(self, coords, params['FRUIT_COLOR'])

    @staticmethod
    def create_random_fruit():
        tile_size = params['TILE_SIZE']
        max_size_x = params['WIN_SIZE'][0] - tile_size
        max_size_y = params['WIN_SIZE'][1] - tile_size
        x = random.randrange(tile_size, max_size_x, tile_size)
        y = random.randrange(tile_size, max_size_y, tile_size)
        return Fruit([x, y])


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
        self.ate_something = None

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
        if not self.ate_something:
            self.body.pop()
        else:
            self.ate_something = False

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

    def eat(self):
        self.ate_something = True

    def draw(self, screen):
        for tile in self.body:
            tile.draw(screen)
        self.head.draw(screen)