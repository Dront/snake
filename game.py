import os
import pygame
import random
from pygame.constants import USEREVENT
from params import params
from snake import Snake, ObstacleContainer, Fruit
import utils


class State(object):
    RUN = 1
    PAUSE = 2
    GAME_OVER = 3


class Game(object):
    """
    This class represents an instance of the game.
    Works like simple state machine.
    """

    UPDATE_SNAKE = USEREVENT + 1

    def __init__(self):
        self.state = State.RUN

        self.player = Snake()
        self.run_snake_timer()

        self.obstacles = ObstacleContainer(filename=params["DEFAULT_MAP"])

        map_size = params['TILE_COUNT']
        self.map = set([(i, j) for i in range(map_size) for j in range(map_size)])
        self.map -= self.obstacles.coords

        self.fruit = pygame.sprite.GroupSingle()
        self.fruit.add(self.create_fruit())

        bg = pygame.image.load(os.path.join(params['PIC_FOLDER'], params['BG_PIC']))
        self.bg_pic = pygame.transform.scale(bg, params['WIN_SIZE'])
        self.bg_pic.set_colorkey((255, 255, 255))

    def create_fruit(self):
        free_tiles = self.map - self.player.coords
        new_coords = random.choice(list(free_tiles))
        return Fruit.create(new_coords)

    def run_snake_timer(self, run=True):
        if run:
            pygame.time.set_timer(self.UPDATE_SNAKE, params['STEP_TIME'])
        else:
            pygame.time.set_timer(self.UPDATE_SNAKE, 0)

    def process_events(self):
        """
        Process all of the events.
        Return True if window must be closed.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == self.UPDATE_SNAKE:
                self.player.go()

            if event.type == pygame.KEYDOWN:

                # esc pressed - quit
                if event.key == pygame.K_ESCAPE:
                    return True

                if self.state == State.RUN:
                    if event.key == pygame.K_UP:
                        self.player.change_dir('UP')
                    elif event.key == pygame.K_DOWN:
                        self.player.change_dir('DOWN')
                    elif event.key == pygame.K_LEFT:
                        self.player.change_dir('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        self.player.change_dir('RIGHT')

                    elif event.key == pygame.K_q:
                        self.state = State.GAME_OVER
                        self.run_snake_timer(False)

                    elif event.key == pygame.K_p:
                        self.state = State.PAUSE
                        self.run_snake_timer(False)

                elif self.state == State.PAUSE:
                    if event.key == pygame.K_q:
                        self.state = State.GAME_OVER
                    else:
                        self.state = State.RUN
                        self.run_snake_timer()

                elif self.state == State.GAME_OVER:
                    self.__init__()

        return False

    def run_logic(self):
        """
        Updates positions.
        """
        if self.state == State.RUN:

            # collision with wall
            if pygame.sprite.spritecollideany(self.player.head, self.obstacles.tiles):
                self.state = State.GAME_OVER

            # collision with tail
            elif pygame.sprite.spritecollideany(self.player.head, self.player.body):
                self.state = State.GAME_OVER

            # ate a fruit
            ate = pygame.sprite.spritecollideany(self.player.head, self.fruit.sprites())
            if ate is not None:
                self.player.eat(ate)
                self.fruit.add(self.create_fruit())

    def display_frame(self, screen):
        """ Display everything to the screen. """
        screen.fill(params['BG_COLOR'])
        # screen.blit(self.bg_pic, (0, 0))

        if self.state == State.GAME_OVER:
            utils.draw_text(screen, params['GAME_OVER_TEXT'])

        elif self.state == State.RUN:
            utils.draw_grid(screen)
            self.obstacles.draw(screen)
            self.fruit.draw(screen)
            self.player.draw(screen)

        elif self.state == State.PAUSE:
            utils.draw_text(screen, params['GAME_PAUSED_TEXT'])

        utils.draw_score(screen, self.player.score)

        pygame.display.flip()
