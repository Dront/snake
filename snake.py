import pygame
import random
import os
from params import params


class Tile(pygame.sprite.Sprite):
    """
    Represents one tile from the grid
    """

    size = params['TILE_SIZE']

    def __init__(self, coords, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pygame.Surface((Tile.size, Tile.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.set_coords(coords)

    def set_coords(self, coords):
        self.coords = coords
        self.rect.x = self.coords[0] * self.size
        self.rect.y = self.coords[1] * self.size


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
        return Fruit((x, y))


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
        self.tiles = pygame.sprite.Group()
        self.coords = []

        if filename is None:
            filename = params['DEFAULT_MAP']

        cur_path = os.getcwd()
        map_path = os.path.join(cur_path, params['MAP_FOLDER'], filename)

        with open(map_path, 'r') as map_file:
            for i, line in enumerate(map_file):
                for j in xrange(params['TILE_COUNT']):
                    if line[j] == '*':
                        c = (j, i)
                        self.coords.append(c)
                        self.tiles.add(Obstacle(c))

    def draw(self, screen):
        self.tiles.draw(screen)


class Snake(object):
    """
    Represents player
    """

    UP = (0, -1)
    DOWN = (0,  1)
    LEFT = (-1, 0)
    RIGHT = (1,  0)

    def __init__(self):
        self.cur_dir = self.UP
        self.size = params['START_SIZE']
        self.next_dir = None
        self.ate_something = None

        self.head = SnakeHead(params['START_POS'])

        self.body = []
        self.coords = [self.head.coords]
        pos = self.head.coords
        for i in range(1, self.size):
            pos = (pos[0] - self.cur_dir[0], pos[1] - self.cur_dir[1])
            self.coords.append(pos)
            self.body.append(SnakeBody(pos))

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.head)
        self.sprites.add(self.body)

    def go(self):
        if self.next_dir is not None:
            self.cur_dir = self.next_dir
            self.next_dir = None

        self.coords = []
        head_coords = tuple(self.head.coords)
        tail_coords = tuple(self.body[-1].coords)

        for i in xrange(len(self.body)-1, 0, -1):
            c = self.body[i-1].coords
            self.body[i].set_coords(c)
            self.coords.append(c)

        self.body[0].set_coords(head_coords)
        self.coords.append(head_coords)

        if self.ate_something:
            new_tile = SnakeBody(tail_coords)
            self.coords.append(tail_coords)
            self.body.append(new_tile)
            self.sprites.add(new_tile)
            self.ate_something = False

        head_x = (head_coords[0] + self.cur_dir[0]) % params['TILE_COUNT']
        head_y = (head_coords[1] + self.cur_dir[1]) % params['TILE_COUNT']
        tmp = (head_x, head_y)
        self.head.set_coords(tmp)
        self.coords.append(tmp)

    def change_dir(self, direction):
        if direction == 'UP':
            if self.cur_dir != self.DOWN:
                self.next_dir = self.UP
        elif direction == 'DOWN':
            if self.cur_dir != self.UP:
                self.next_dir = self.DOWN
        elif direction == 'LEFT':
            if self.cur_dir != self.RIGHT:
                self.next_dir = self.LEFT
        elif direction == 'RIGHT':
            if self.cur_dir != self.LEFT:
                self.next_dir = self.RIGHT

    def eat(self):
        self.ate_something = True

    def draw(self, screen):
        self.sprites.draw(screen)