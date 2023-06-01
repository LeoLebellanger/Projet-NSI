import pygame
import os
from constants import const
from vguis import *
from entities import *
from chunck import Chunck, loadTileTypes
import time
import math
ratioX, ratioY = const["SCREEN_SIZE"][0] / const["CHUNCK_SIZE"], const["SCREEN_SIZE"][1] / const["CHUNCK_SIZE"]

class Game:
    def __init__(self):
        loadTileTypes()
        self.isRunning = False 
        self.isInExitMenu = False
        self.entities = []
        self.vguis = []
        self.assests = {}
        self.chuncks = {}
        self.loadAssets("player")
        self.openExitMenu()
        self.player = Player(self)
        self.addEntitie(self.player)
        self.clock = pygame.time.Clock()
        self.pressedKeys = {}
        self.camPos = [0, 0]
        self.backgroundImage = pygame.transform.scale(pygame.image.load("assets/background/background.png").convert_alpha(), const["SCREEN_SIZE"])

    def resume(self):
        self.isRunning = True

    def pause(self):
        self.isRunning = False 

    def draw(self, screen, image, pos, size):
        screen.blit(image, (pos[0] - self.camPos[0], pos[1] - self.camPos[1], *size))

    def drawRect(self, screen, color, pos, size):
        pygame.draw.rect(screen, color, (pos[0] - self.camPos[0], pos[1] - self.camPos[1], *size))
    
    def isInCamView(self, pos):
        return abs(self.camPos[0] - pos[0]) < const["SCREEN_SIZE"][0] and abs(self.camPos[1] - pos[1]) < const["SCREEN_SIZE"][1]

    def updateCamPos(self):
        self.camPos[0], self.camPos[1] = self.player.pos[0] + self.player.size[0]/2 - const["SCREEN_SIZE"][0]/2, self.player.pos[1] + self.player.size[1]/2 + - const["SCREEN_SIZE"][1]/1.5# Player is in the center of the screen

    # Main func
    def update(self, screen):
        self.clock.tick(const["FPS"])
        for vgui in self.getVguis():
            vgui.paint(screen)
        
        if self.isInExitMenu: return

        screen.blit(self.backgroundImage, (0, 0))

        for i in range(2):
            for j in range(2):
                x, y = int((self.camPos[0] + const["SCREEN_SIZE"][0]*i)//const["SCREEN_SIZE"][0]), int((self.camPos[1] + const["SCREEN_SIZE"][1]*j)//const["SCREEN_SIZE"][1])
                if not self.chuncks.get(f"{x}:{y}"):
                    self.generateNewChunck(x, y)
                self.chuncks[f"{x}:{y}"].draw(screen)

        for ent in self.getEntities():
            ent.update()
            ent.nextSequence()
            ent.draw(screen)

        if self.isRunning: pass 

    def openExitMenu(self):
        self.isRunning = False
        self.isInExitMenu = True 

        startButton = Button()
        self.addVgui(startButton)
        startButton.setText("Commencer")
        startButton.setTextColor((0, 0, 0))
        startButton.click = lambda : self.closeExitMenu()
    
    def closeExitMenu(self):
        self.isRunning = True
        self.isInExitMenu = False 

        self.clearVguis()

    def addEntitie(self, ent):
        self.entities.append(ent)

    def addVgui(self, vgui):
        self.vguis.append(vgui)

    def clearVguis(self):
        self.vguis = []

    def generateNewChunck(self, x ,y):
        chunck = Chunck(self, x, y)
        self.chuncks[f"{x}:{y}"] = chunck

    def loadAssets(self, name=None):
        if not name:
            for name in os.listdir("assets"):
                self.loadAssets(name)
            return
        
        assets = self.getAssets()

        assets[name] = {}
        for assetsType in os.listdir(f"assets/{name}"):
            assets[name][assetsType] = {}
            assets[name][assetsType]["RIGHT"] = []
            assets[name][assetsType]["LEFT"] = []
            dirs = os.listdir(f"assets/{name}/{assetsType}")
            ratio = math.floor(const["FPS"] / len(dirs))
            for fileName in dirs:
                image = pygame.image.load(f"assets/{name}/{assetsType}/{fileName}").convert_alpha()
                assets[name][assetsType]["RIGHT"] += [image] * ratio
                assets[name][assetsType]["LEFT"] += [pygame.transform.flip(image, True, False)] * ratio

    # [Accessors]
    # [Getters]
    def getEntities(self):
        return self.entities

    def getVguis(self):
        return self.vguis
    
    def getChuncks(self):
        return self.chuncks
    
    def getAssets(self, name=None, assetsType=None):
        if name:
            if assetsType: return self.assests[name][assetsType]
            else: return self.assests[name]
        else: return self.assests

    def getPressedKeys(self):
        return self.pressedKeys