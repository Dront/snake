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

        pic = pygame.image.load(os.path.join(params['PIC_FOLDER'], params['WALL_PIC']))
        pic = pygame.transform.scale(pic, (Tile.size, Tile.size)).convert()
        self.image = pic


class Ground(Tile):
    """
    Class represents free tiles on map. Convenience class.
    """

    def __init__(self, coords):
        Tile.__init__(self, coords, params['GROUND_COLOR'])

        pic = pygame.image.load(os.path.join(params['PIC_FOLDER'], params['GROUND_PIC']))
        pic = pygame.transform.scale(pic, (Tile.size, Tile.size)).convert()
        self.image = pic


class Fruit(Tile):
    """
    Class represents fruits for snake.
    """

    pics = params['FRUIT_PICS']
    weights = params['FRUIT_WEIGHTS']

    def __init__(self, coords, weight=1, pic=pics[0]):
        Tile.__init__(self, coords, params['FRUIT_COLOR'])
        self.weight = weight
        pic = pygame.image.load(os.path.join(params['PIC_FOLDER'], pic))
        pic = pygame.transform.scale(pic, (Tile.size, Tile.size)).convert_alpha()
        self.image = pic

    @staticmethod
    def create(coords):
        index = random.randrange(len(Fruit.pics))
        return Fruit(coords, weight=Fruit.weights[index], pic=Fruit.pics[index])


class SnakeHead(Tile):
    def __init__(self, coords):
        Tile.__init__(self, coords, params['HEAD_COLOR'])


class SnakeBody(Tile):
    def __init__(self, coords):
        Tile.__init__(self, coords, params['BODY_COLOR'])


class Map(object):
    """
    Represents all obstacle on map
    """

    def __init__(self, filename=params['DEFAULT_MAP']):
        self.obstacles = pygame.sprite.Group()
        self.ground = pygame.sprite.Group()
        self.obs_coords = set()
        self.ground_coords = set()

        cur_path = os.getcwd()
        map_path = os.path.join(cur_path, params['MAP_FOLDER'], filename)

        with open(map_path, 'r') as map_file:
            for i, line in enumerate(map_file):
                for j in xrange(params['TILE_COUNT']):
                    c = (j, i)
                    if line[j] == '*':
                        self.obs_coords.add(c)
                        self.obstacles.add(Obstacle(c))
                    elif line[j] == '-':
                        self.ground_coords.add(c)
                        self.ground.add(Ground(c))

    def draw(self, screen):
        self.obstacles.draw(screen)
        self.ground.draw(screen)


class Snake(object):
    """
    Represents player
    """

    UP = (0, -1)
    DOWN = (0,  1)
    LEFT = (-1, 0)
    RIGHT = (1,  0)

    def __init__(self):
        self.score = 0
        self.cur_dir = self.UP
        self.size = params['START_SIZE']
        self.next_dir = None
        self.ate_something = None

        self.head = SnakeHead(params['START_POS'])

        self.body = []
        self.coords = set(self.head.coords)
        pos = self.head.coords
        for i in range(1, self.size):
            pos = (pos[0] - self.cur_dir[0], pos[1] - self.cur_dir[1])
            self.coords.add(pos)
            self.body.append(SnakeBody(pos))

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.head)
        self.sprites.add(self.body)

    def go(self):
        if self.next_dir is not None:
            self.cur_dir = self.next_dir
            self.next_dir = None

        self.coords = set()
        head_coords = tuple(self.head.coords)
        tail_coords = tuple(self.body[-1].coords)

        for i in xrange(len(self.body)-1, 0, -1):
            c = self.body[i-1].coords
            self.body[i].set_coords(c)
            self.coords.add(c)

        self.body[0].set_coords(head_coords)
        self.coords.add(head_coords)

        if self.ate_something:
            new_tile = SnakeBody(tail_coords)
            self.coords.add(tail_coords)
            self.body.append(new_tile)
            self.sprites.add(new_tile)
            self.ate_something = False

        head_x = (head_coords[0] + self.cur_dir[0]) % params['TILE_COUNT']
        head_y = (head_coords[1] + self.cur_dir[1]) % params['TILE_COUNT']
        tmp = (head_x, head_y)
        self.head.set_coords(tmp)
        self.coords.add(tmp)

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

    def eat(self, fruit):
        self.score += fruit.weight
        self.ate_something = True

    def draw(self, screen):
        self.sprites.draw(screen)
