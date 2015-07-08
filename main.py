#!usr/bin/python

import pygame
from game import Game
from params import params


def main():
    pygame.init()

    screen = pygame.display.set_mode(params['WIN_SIZE'])
    pygame.display.set_caption(params['CAPTION'])

    pygame.mouse.set_visible(True)
    pygame.mouse.set_cursor(*pygame.cursors.diamond)

    done = False
    clock = pygame.time.Clock()

    game = Game()

    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(params['FPS'])

    pygame.quit()


if __name__ == '__main__':
    main()