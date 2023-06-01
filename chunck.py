import pygame
import os
import random
from constants import const
ratioX, ratioY = const["SCREEN_SIZE"][0] / const["CHUNCK_SIZE"], const["SCREEN_SIZE"][1] / const["CHUNCK_SIZE"]

tileTypes = []
def loadTileTypes():
    tileTypes.append([pygame.transform.scale(pygame.image.load(f"assets/tiles/dirt/{image}").convert_alpha(), (ratioX, ratioY)) for image in os.listdir("assets/tiles/dirt")])
    tileTypes.append([pygame.transform.scale(pygame.image.load(f"assets/tiles/grass/{image}").convert_alpha(), (ratioX, ratioY)) for image in os.listdir("assets/tiles/grass")])

class Tile:
    def __init__(self, game, chunck, image, pos, type):
        self.game = game 
        self.image = image
        self.chunck = chunck
        self.rect = image.get_rect()
        self.rect.x = pos[0]*ratioX
        self.rect.y = pos[1]*ratioY
        self.pos = pos 
        self.type = type

    def draw(self, screen):
        self.game.draw(screen, self.image, self.chunck.localToWorld(self.pos), [ratioX, ratioY])
        

class Chunck:
    def __init__(self, game, x, y):
        self.game = game
        self.tiles = []
        self.pos = [x*const["SCREEN_SIZE"][0], y*const["SCREEN_SIZE"][1]]
        self.generate(x, y)

    def draw(self, screen):
        for tile in self.getTiles():
            pos = self.localToWorld(tile.pos)
            if not self.game.isInCamView(pos): continue
            tile.draw(screen)
    
    def localToWorld(self, pos):
        return self.pos[0] + pos[0], self.pos[1] + pos[1]

    def generate(self, x, y): # Very simple generation
        for yPos in range(const["CHUNCK_SIZE"]):
            for xPos in range(const["CHUNCK_SIZE"]):
                tarX, tarY = x * const["CHUNCK_SIZE"] + xPos, y * const["CHUNCK_SIZE"] + yPos
                tileType = 0
                if tarY > int(const["CHUNCK_SIZE"]*0.4):
                    tileType = 1
                elif tarY == int(const["CHUNCK_SIZE"]*0.4):
                    tileType = 2
                elif tarY < int(const["CHUNCK_SIZE"]*0.4) - 1 and random.randint(1, 20) == 10:
                    tileType = 2

                if tileType == 0: continue
                tile = Tile(self.game, self, tileTypes[tileType-1][random.randrange(len(tileTypes[tileType-1]))], [xPos*ratioX, yPos*ratioY], tileType)
                self.tiles.append(tile)

    # [Accessors funcs]
    # [Getters]
    def getTiles(self):
        return self.tiles
    
    def getPos(self):
        return self.pos