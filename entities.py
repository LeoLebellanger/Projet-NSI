import pygame
from constants import const
from utils import lerp
from math import dist

class Entity(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.sequence = ""
        self.sequenceCount = 0
        self.sequenceInfos = {}
        self.sequences = {}
        self.direction = "RIGHT"
        self.setPos(0, 0)
        self.setSize(50, 50)
        self.setColor((255, 255, 255))
        self.setHealth(-1) # -1 = god mode
        self.setVelocity(0)
        self.setAirVelocity(0) # Jump
        self.gravity = 0

    def draw(self, screen):
        self.game.draw(screen, self.getImage(), self.getPos(), self.getSize())

    def update(self):
        self.rect = pygame.Rect(*self.getPos(), *self.getSize())

    def nextSequence(self):
        seqCount = self.getSequenceCount()
        if seqCount + 1 >= self.getSequenceInfos()["nSeq"]:
            self.setSequenceCount(0)
        else:
            self.setSequenceCount(seqCount + 1)

    def isCollinding(self, targetRect: pygame.Rect):
        if abs(self.pos[0] - targetRect.right) < 3:
            return True, "left"
        elif abs(self.pos[0] + self.size[0] - targetRect.left) < 3:
            return True, "right"
        elif abs(self.pos[1] - targetRect.bottom) < 3:
            return True, "top"
        elif abs(self.pos[1] + self.size[1] - targetRect.top) < 3:
            return True, "bottom"
    
        return False, ""

    # [Accessors]
    # [Getters]
    def getPos(self):
        return self.pos

    def getSize(self):
        return self.size
    
    def getColor(self):
        return self.color

    def getSequences(self, name=None):
        if name: return self.sequences[name]
        else: return self.sequences
    
    def getSequence(self):
        return self.sequence
    
    def getSequenceInfos(self):
        return self.sequenceInfos
    
    def getSequenceCount(self):
        return self.sequenceCount
    
    def getHealth(self):
        return self.health
    
    def getDirection(self):
        return self.direction
    
    def getVelocity(self):
        return self.velocity
    
    def getAirVelocity(self):
        return self.airVelocity

    def getImage(self):
        return self.sequences[self.getSequence()][self.getDirection()][self.getSequenceCount()]
    
    def getGravity(self):
        return self.gravity
    
    def getActiveChunck(self):
        x, y = int(self.rect.x//const["SCREEN_SIZE"][0]), int(self.rect.y//const["SCREEN_SIZE"][1])
        return self.game.chuncks[f"{x}:{y}"]


    def getCollisions(self):
        collisions = {}
        for tile in self.getActiveChunck().getTiles():
            if not self.rect.colliderect(tile["rect"]): continue
            colBottom = False
            if abs(tile["rect"].top - self.rect.bottom) < 15:
                collisions["bottom"] = True
                colBottom = True
            elif abs(tile["rect"].bottom - self.rect.top) < 15:
                collisions["top"] = True

            if abs(tile["rect"].left - self.rect.right) < 15 and not colBottom:
                collisions["right"] = True 
            if abs(tile["rect"].right - self.rect.left) < 15 and not colBottom:
                collisions["left"] = True

        return collisions

    # [Setters]
    def setPos(self, x, y):
        self.pos = [x, y]

    def setSize(self, w, h):
        self.size = [w, h]
        for sequence in self.sequences:
            for k, image in enumerate(self.sequences[sequence]["LEFT"]):
                self.sequences[sequence]["LEFT"][k] = pygame.transform.scale(image, (w, h))
            for k, image in enumerate(self.sequences[sequence]["RIGHT"]):
                self.sequences[sequence]["RIGHT"][k] = pygame.transform.scale(image, (w, h))

    def setColor(self, color):
        self.color = color

    def setSequences(self, sequences):
        self.sequences = sequences

    def setSequence(self, sequence):
        self.sequence = sequence
        self.setSequenceCount(0) # Reset count
        self.setSequenceInfos({
            "nSeq" : len(self.sequences[self.sequence][self.direction])
        })

    def setSequenceInfos(self, infos):
        self.sequenceInfos = infos

    def setSequenceCount(self, count):
        self.sequenceCount = count

    def setHealth(self, health):
        self.health = health

    def setDirection(self, direction):
        self.direction = direction

    def setVelocity(self, velocity):
        self.velocity = velocity

    def setAirVelocity(self, airVelocity):
        self.airVelocity = airVelocity

class Player(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.setSequences(game.getAssets()["player"])
        self.setSequence("idle")
        self.setHealth(100)
        self.setVelocity(7)
        self.setAirVelocity(12)
        self.setSize(100, 70)
        self.setPos(0, 0)
        self.rect = self.getImage().get_rect()

    def draw(self, screen):
        self.game.draw(screen, self.getImage(), (self.rect.x, self.rect.y), (self.rect.w, self.rect.h))
        self.game.drawRect(screen, (255, 0, 0), (self.rect.x, self.rect.y), (self.getHealth()*0.8, 5))

    def attack(self):
        if self.getSequence() == "idle": self.setSequence("attack")

    def update(self):
        pressedKeys = self.game.getPressedKeys()
        currentSeq = self.getSequence()
        direction = self.getDirection()
        collisions = self.getCollisions()
        if pressedKeys.get(pygame.K_LEFT):
            if currentSeq != "run": self.setSequence("run")
            if direction != "LEFT" : self.setDirection("LEFT")
            if not collisions.get("left"):
                self.rect.x -= self.velocity
        elif pressedKeys.get(pygame.K_RIGHT):
            if currentSeq != "run": self.setSequence("run")
            if direction != "RIGHT" : self.setDirection("RIGHT")
            if not collisions.get("right"):
                self.rect.x += self.velocity
        elif pressedKeys.get(pygame.K_SPACE):
            if currentSeq != "jump": self.setSequence("jump")
            if self.getSequenceCount() > 2/3*const["FPS"] and not collisions.get("top"):
                self.rect.y -= self.getAirVelocity()
        elif pressedKeys.get(pygame.K_DOWN):
            self.rect.y += self.getAirVelocity()
        elif currentSeq == "attack":
            pass
        else:
            if currentSeq != "idle": self.setSequence("idle")

        #gravity
        if collisions.get("bottom"):
            self.gravity = 1
        else:
            self.gravity = lerp(0.1, self.gravity, 5)
            self.rect.y += self.gravity

        self.game.updateCamPos()