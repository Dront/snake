#!/usr/bin/python

import pygame
from params import params


screen = pygame.display.set_mode(params['WIN_SIZE'])
pygame.display.set_caption(params['CAPTION'])

from game import Game
from res import res


def main():
    pygame.init()

    pygame.display.set_icon(res['ICON'])
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
