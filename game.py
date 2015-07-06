import pygame
from pygame.constants import USEREVENT
from params import params
from snake import Snake

# TODO
# creates game states for some customizing

class Game(object):
    """
    This class represents an instance of the game.
    """

    UPDATE_SNAKE = USEREVENT + 1

    def __init__(self):
        self.score = 0
        self.game_over = False
        self.player = Snake()
        pygame.time.set_timer(self.UPDATE_SNAKE, params['STEP_TIME'])

    def process_events(self):
        """
        Process all of the events.
        Returns True if window must be closed.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == self.UPDATE_SNAKE:
                self.player.go()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                elif event.key == pygame.K_q:
                    self.game_over = True
                elif event.key == pygame.K_UP:
                    self.player.change_dir('UP')
                elif event.key == pygame.K_DOWN:
                    self.player.change_dir('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.player.change_dir('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.player.change_dir('RIGHT')

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()

        return False

    def run_logic(self):
        """
        Updates positions.
        """
        if not self.game_over:
            pass

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(params['BG_COLOR'])

        if self.game_over:
            font = pygame.font.Font(None, 25)
            text = font.render(params['GAME_OVER_TEXT'], True, params['TEXT_COLOR'])
            center_x = (params['WIN_SIZE'][0] // 2) - (text.get_width() // 2)
            center_y = (params['WIN_SIZE'][1] // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])
        else:
            self.player.draw(screen)

        pygame.display.flip()