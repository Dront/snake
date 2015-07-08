import pygame
import random
from params import params


class Tile(pygame.sprite.Sprite):
    """
    Represents one tile from the grid
    """

    def __init__(self, coords, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.coords = coords

        size = params['TILE_SIZE']
        self.image = pygame.Surface([size, size])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.coords[0] * size
        self.rect.y = self.coords[1] * size


class Obstacle(Tile):
    """
    Class represents obstacles on map. Convenience class.
    """

    def __init__(self, coords):
        Tile.__init__(self, coords, params['OBSTACLE_COLOR'])


class Fruit(Tile):
    """
    Class represents fruits for snake.
    """

    def __init__(self, coords):
        Tile.__init__(self, coords, params['FRUIT_COLOR'])

    @staticmethod
    def create_random_fruit():
        max_size_x = params['TILE_COUNT'] - 1
        x = random.randrange(1, max_size_x)
        y = random.randrange(1, max_size_x)
        return Fruit([x, y])


class SnakeHead(Tile):
    def __init__(self, coords):
        Tile.__init__(self, coords, params['HEAD_COLOR'])


class SnakeBody(Tile):
    def __init__(self, coords):
        Tile.__init__(self, coords, params['BODY_COLOR'])


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

        self.tiles = pygame.sprite.Group()

        if filename is None:
            tile_count = params['TILE_COUNT']

            for x in range(0, tile_count):
                self.tiles.add(Obstacle([x, 0]))
                self.tiles.add(Obstacle([x, tile_count - 1]))

            for y in range(1, tile_count - 1):
                self.tiles.add(Obstacle([0, y]))
                self.tiles.add(Obstacle([tile_count - 1, y]))

        else:
            raise NotImplementedError

    def draw(self, screen):
        self.tiles.draw(screen)


class Snake(object):
    """
    Represents player
    """

    UP = [0, -1]
    DOWN = [0,  1]
    LEFT = [-1, 0]
    RIGHT = [1,  0]

    def __init__(self):
        self.cur_dir = self.UP
        self.size = params['START_SIZE']
        self.next_dir = None
        self.ate_something = None

        self.head = SnakeHead(params['START_POS'])

        self.body = []
        pos = self.head.coords
        for i in range(1, self.size):
            pos = [pos[0] - self.cur_dir[0], pos[1] - self.cur_dir[1]]
            self.body.append(SnakeBody(pos))

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.head)
        self.sprites.add(self.body)

    def go(self):
        if self.next_dir is not None:
            self.cur_dir = self.next_dir
            self.next_dir = None

        tmp_coords = list(self.head.coords)

        new_tile = SnakeBody(tmp_coords)

        self.body.insert(0, new_tile)
        self.sprites.add(new_tile)

        if not self.ate_something:
            tmp = self.body.pop()
            self.sprites.remove(tmp)
        else:
            self.ate_something = False

        tmp_coords = [tmp_coords[0] + self.cur_dir[0], tmp_coords[1] + self.cur_dir[1]]

        self.sprites.remove(self.head)
        self.head = SnakeHead(tmp_coords)
        self.sprites.add(self.head)

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
        self.sprites.draw(screen)