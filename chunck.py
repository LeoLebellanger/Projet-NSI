import pygame
import os
import random
from constants import const
ratioX, ratioY = const["SCREEN_SIZE"][0] / const["CHUNCK_SIZE"], const["SCREEN_SIZE"][1] / const["CHUNCK_SIZE"]

tileTypes = []
def loadTileTypes():
    tileTypes.append([pygame.transform.scale(pygame.image.load(f"assets/tiles/dirt/{image}").convert_alpha(), (ratioX, ratioY)) for image in os.listdir("assets/tiles/dirt")])
    tileTypes.append([pygame.transform.scale(pygame.image.load(f"assets/tiles/grass/{image}").convert_alpha(), (ratioX, ratioY)) for image in os.listdir("assets/tiles/grass")])

class Chunck:
    def __init__(self, game, x, y):
        self.game = game
        self.tiles = []
        self.pos = [x*const["SCREEN_SIZE"][0], y*const["SCREEN_SIZE"][1]]
        self.generate(x, y)

    def draw(self, screen):
        for tile in self.getTiles():
            pos = self.localToWorld(tile["pos"])
            if not self.game.isInCamView(pos): continue
            self.game.draw(screen, tile["image"], pos, [ratioX, ratioY])
    
    def localToWorld(self, pos):
        return self.pos[0] + pos[0], self.pos[1] + pos[1]
    
    def getEntities(self):
        ents = []
        for ent in self.game.getEntities():
            x, y = ent.getPos()
            if x >= self.pos[0] and x <= self.pos[0] + const["CHUNCK_SIZE"]*ratioX and y >= self.pos[1] and y <= self.pos[1] + const["CHUNCK_SIZE"]*ratioY:
                ents.append(ent)
        return ents

    def generate(self, x, y): # Very simple generation
        for yPos in range(const["CHUNCK_SIZE"]):
            for xPos in range(const["CHUNCK_SIZE"]):
                tarX, tarY = x * const["CHUNCK_SIZE"] + xPos, y * const["CHUNCK_SIZE"] + yPos
                tileType = 0
                if tarY > int(const["CHUNCK_SIZE"]*0.4):
                    tileType = 1
                elif tarY == int(const["CHUNCK_SIZE"]*0.4):
                    tileType = 2
                elif tarY < int(const["CHUNCK_SIZE"]*0.4) - 1 and tarY > 0 and random.randint(1, 100) == 10:
                    tileType = 2

                if tarY == int(const["CHUNCK_SIZE"]*0.4) - 4 and random.randint(0, 2) == 1:
                    self.game.spawnMummy(tarX*const["SCREEN_SIZE"][0], tarY*const["SCREEN_SIZE"][1])

                if tileType == 0: continue
                self.tiles.append({
                    "pos": [xPos*ratioX, yPos*ratioY],
                    "rect": pygame.Rect(tarX*ratioX, tarY*ratioY, ratioX, ratioX),
                    "type": tileType,
                    "image": tileTypes[tileType-1][random.randrange(len(tileTypes[tileType-1]))]
                })

    # [Accessors funcs]
    # [Getters]
    def getTiles(self):
        return self.tiles
    
    def getPos(self):
        return self.pos