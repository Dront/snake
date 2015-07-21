#!/usr/bin/python

import os
import pygame
from game import Game
from params import params


def main():
    pygame.init()

    # the cursor
    pygame.mouse.set_visible(True)
    pygame.mouse.set_cursor(*pygame.cursors.diamond)

    screen = pygame.display.set_mode(params['WIN_SIZE'])
    pygame.display.set_caption(params['CAPTION'])

    icon = pygame.image.load(os.path.join(params['PIC_FOLDER'], params['ICON'])).convert_alpha()
    pygame.display.set_icon(icon)

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
