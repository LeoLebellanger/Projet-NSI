# [Made by Léo Lebellanger with ♥️]

import pygame
from constants import const
from game import Game

screen = pygame.display.set_mode(const["SCREEN_SIZE"])
game = Game()
running = True 
while running: # Boucle principale
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1: continue
            for vgui in game.getVguis()[::-1]:
                if vgui.__class__.__name__ == "Button" and vgui.isHovered(event.pos):
                    vgui.click()
                    break
            else:
                if not game.isInExitMenu: 
                    game.player.attack() # player attack
        elif event.type == pygame.KEYDOWN:
            game.pressedKeys[event.key] = True 
        elif event.type == pygame.KEYUP:
            del game.pressedKeys[event.key] 

    # Clear de l'écran
    screen.fill(const["BACKGROUND_COLOR"])
    game.update(screen)
    pygame.display.flip()