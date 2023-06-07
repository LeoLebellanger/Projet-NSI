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
        self.loadAssets("mummy", True)
        self.openExitMenu()
        self.clock = pygame.time.Clock()
        self.pressedKeys = {}
        self.camPos = [0, 0]
        self.backgroundImage = pygame.transform.scale(pygame.image.load("assets/background/background.png").convert_alpha(), const["SCREEN_SIZE"])
        self.player = None

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
        self.camPos[0], self.camPos[1] = self.player.rect.x + self.player.rect.w/2 - const["SCREEN_SIZE"][0]/2, self.player.rect.y + self.player.rect.h/2 - const["SCREEN_SIZE"][1]/1.5# Player is in the center of the screen

    # Main func
    def update(self, screen):
        if not self.player or self.player.getHealth() <= 0 and not self.isInExitMenu: 
            self.player = None
            self.clearVguis()
            self.clearEntities()
            self.clearChuncks()
            self.openExitMenu()
        screen.blit(self.backgroundImage, (0, 0))
        self.clock.tick(const["FPS"])
        for vgui in self.getVguis():
            vgui.paint(screen)
        
        if self.isInExitMenu: return

        for i in range(2):
            for j in range(2):
                x, y = int((self.camPos[0] + const["SCREEN_SIZE"][0]*i)//const["SCREEN_SIZE"][0]), int((self.camPos[1] + const["SCREEN_SIZE"][1]*j)//const["SCREEN_SIZE"][1])
                if not self.chuncks.get(f"{x}:{y}"):
                    self.generateNewChunck(x, y)
                self.chuncks[f"{x}:{y}"].draw(screen)

        xp = self.player.xp
        pygame.draw.rect(screen, (0, 220, 0), (const["SCREEN_SIZE"][0]/2-xp/2, 10, xp, 10))

        for ent in self.getEntities():
            if not self.isInCamView(ent.getPos()): continue
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
        startButton.setHoveredColor((255, 0, 0))
        startButton.setSize(100, 50)
        startButton.setPos(400, 275)
        startButton.click = lambda : self.spawnPlayer() or self.closeExitMenu()
    
    def closeExitMenu(self):
        self.isRunning = True
        self.isInExitMenu = False 

        self.clearVguis()

    def spawnPlayer(self):
        self.player = Player(self)
        self.player.setPos(0, 0)
        self.addEntitie(self.player)
        self.updateCamPos()

    def addEntitie(self, ent):
        self.entities.append(ent)

    def addVgui(self, vgui):
        self.vguis.append(vgui)

    def clearVguis(self):
        self.vguis = []

    def clearEntities(self):
        self.entities = []

    def clearChuncks(self):
        self.chuncks = {}

    def generateNewChunck(self, x ,y):
        chunck = Chunck(self, x, y)
        self.chuncks[f"{x}:{y}"] = chunck

    def loadAssets(self, name=None, revert=False):
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

                if revert:
                    assets[name][assetsType]["RIGHT"] += [pygame.transform.flip(image, True, False)] * ratio
                    assets[name][assetsType]["LEFT"] += [image] * ratio
                else:
                    assets[name][assetsType]["RIGHT"] += [image] * ratio
                    assets[name][assetsType]["LEFT"] += [pygame.transform.flip(image, True, False)] * ratio
            
    def spawnMummy(self, x, y):
        mummy = Mummy(self)
        mummy.setPos(x, y)
        self.addEntitie(mummy)

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