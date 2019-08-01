import pygame

class renderable:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.pos = (x, y)
    def draw(self, screen):
        pass

class rectrenderable(renderable):
    def __init__(self, x, y, w, h, color = (0,0,0)):
        super().__init__(x, y)
        self.w, self.h = w, h
        self.rect = (x, y, w, h)
        self.color = color
    def draw (self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
class circlerenderable(renderable):
    def __init__(self, x, y, r, color = (0,0,0)):
        super().__init__(x, y)
        self.color = color
        self.r = r
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
    
class textrenderable(renderable):
    def __init__(self, x, y, color, font, textfun):
        super().__init__(x, y)
        self.color = color
        self.font = font
        self.textfun = textfun

    def draw(self, screen):
        txt = self.font.render(self.textfun(), True, self.color)
        screen.blit(txt, (self.x, self.y))

class barrenderable(rectrenderable):
    def __init__(self, x, y, w, h, bgcolor, fgcolor, numfun, bordered = False):
        super().__init__(x, y, w, h)
        self.bgcolor, self.fgcolor = bgcolor, fgcolor
        self.bordered = bordered
        self.numfun = numfun

    def draw(self, screen):
        pygame.draw.rect(screen, self.bgcolor, (self.x, self.y, self.w, self.h), 1 if self.bordered else 0)
        (curr, max) = self.numfun()
        pygame.draw.rect(screen, self.fgcolor, (self.x, self.y, round(self.w * curr / max), self.h))

class playerrenderable(rectrenderable):
    def __init__(self, plr):
        super().__init__(plr.x - 50, plr.y - 50, 100, 100)
        self.plr = plr
    
    def draw(self, screen):
        #the player:
        if self.plr.stage == 1:
            pygame.draw.circle(screen, self.plr.color, self.plr.pos, 50)
        else:
            pygame.draw.rect(screen, self.plr.color, self.rect)

        #olhinhos
        (x, y) = self.plr.pos
        pygame.draw.circle(screen, (0,0,0), (x-10, y-30), 5)
        pygame.draw.circle(screen, (0,0,0), (x-10, y-30), 1)
        
        pygame.draw.circle(screen, (0,0,0), (x+10, y-30), 5)
        pygame.draw.circle(screen, (0,0,0), (x+10, y-30), 1)
        
        