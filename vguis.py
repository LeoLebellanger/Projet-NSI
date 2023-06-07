import pygame
pygame.font.init()

fonts = {}
def font(name="Roboto", size=10, weight=500):
    fontName = f"{name}:{size}:{weight}"
    if not fonts.get(fontName):
        fonts[fontName] = pygame.font.SysFont(name, size)
    return fontName

class Panel:
    def __init__(self):
        self.setPos(50, 50)
        self.setSize(50, 50)
        self.setColor((255, 255, 255))
        self.setHoveredColor((255, 255, 255))

    def paint(self, screen):
        if self.isHovered():
            pygame.draw.rect(screen, self.getHoveredColor(), (*self.getPos(), *self.getSize()))
        else:
            pygame.draw.rect(screen, self.getColor(), (*self.getPos(), *self.getSize()))

    def isHovered(self, pos=None):
        if not pos: pos = pygame.mouse.get_pos()
        sPos = self.getPos()
        sSize = self.getSize()
        return pos[0] >= sPos[0] and pos[0] <= sPos[0] + sSize[0] and pos[1] >= sPos[1] and pos[1] <= sPos[1] + sSize[1]

    # [Accessors]
    # [Getters]
    def getPos(self):
        return self.pos

    def getSize(self):
        return self.size
    
    def getColor(self):
        return self.color
    
    def getHoveredColor(self):
        return self.hoveredColor

    # [Setters]
    def setPos(self, x, y):
        self.pos = (x, y)

    def setSize(self, w, h):
        self.size = (w, h)

    def setColor(self, color):
        self.color = color

    def setHoveredColor(self, color):
        self.hoveredColor = color

class Button(Panel):
    def __init__(self):
        super().__init__()
        self.setText("")
        self.setTextColor((255, 255, 255))
        self.setFont(font("Arial", 12, 500))

    def paint(self, screen):
        if self.isHovered():
            pygame.draw.rect(screen, self.getHoveredColor(), (*self.getPos(), *self.getSize()))
        else:
            pygame.draw.rect(screen, self.getColor(), (*self.getPos(), *self.getSize()))
        text = fonts[self.getFont()].render(self.getText(), True, self.getTextColor())
        screen.blit(text, (self.pos[0] + self.size[0]/2 - text.get_rect().w/2, self.pos[1] + self.size[1]/2 - text.get_rect().h/2, *self.getSize()))

    # [Accessors funcs]
    # [Getters]
    def getText(self):
        return self.text 
    
    def getTextColor(self):
        return self.textColor
    
    def getFont(self):
        return self.font

    # [Setters]
    def setText(self, text):
        self.text = text 

    def setTextColor(self, textColor):
        self.textColor = textColor
    
    def setFont(self, font):
        self.font = font 

    def click(self):
        pass