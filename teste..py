#teste
import random as R
import sys
import pygame
import math

pygame.init()

#width = pygame.display.info()[current_w]
#print(str(width))
width = 800
height = 600

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((width, height))
#screen = pygame.display.set_mode((200, 60))


global players
players = []



class player(object):
    def __init__(self,x ,y, name = "none", color = "none"):
        self.pos = (x, y)
        self.MaxHP = 5
        self.HP = 5
        self.abilities = ["Tackle"]
        self.EXP = 0
        self.stage = 1
        
        if color == "none":
            self.color = (R.randint(0,255), R.randint(0,255), R.randint(0,255))
        else:
            self.color = color
            
        if name == "none":
            self.name = R.randint(0,999)
        else:
            self.name = name
            
        players.append(self)
        
    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, 50)
        pygame.draw.rect(screen, (255,0,0), (self.pos[0]-50, self.pos[1]-60, 100, 10))
        pygame.draw.rect(screen, (0,255,0), (self.pos[0]-50, self.pos[1]-60, round((self.HP/self.MaxHP)*100), 10))
        pygame.display.update()


class chooseability(object):
    def __init__(self):
        self.ability = 0
        self.name = "choose ability"
        self.time = 30
        self.time1 = 30
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))

    def clock(self):
        #texttime = fonttime.render(self.name + str(time), 1, (255,0,0))
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)

    def draw(self):

        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))

        #ability tab: 
        pygame.draw.rect(screen, (255,246,143),(0 ,0 ,300 , height))

        #primeira abilidade, por enquanto, tackle:
        pygame.draw.rect(screen, (199,97,20),(10,10, 280, 30))
        screen.blit(texttackle,(100,15))
                     #
        
        screen.blit(self.texttime, (300, 10))
        screen.blit(textround, (300, 30))
        for player in players:
            player.draw()
            
        pygame.display.update()

    

    def receiveevent(self, event):
        mouseposition = event.pos
        print(mouseposition)
        if 10 <= mouseposition[0]  <= 290 and 10 <= mouseposition[1] <= 40: #clicou en tackle:
            print("aqui")
            self.ability = "Tackle"
            #Tackle(choosetarget(1)[0])
            #decided = True
            roundphase = choosetarget(self.ability)

class choosetarget(object):
    def __init__(self, ability):
        self.target = craos
        self.ability = ability
        self.name = "choose target"
        self.time = 30
        self.time1 = 30
        self.texttime = fonttime.render(self.name + str(self.time), 1, (255,0,0))

    def clock(self):
        #texttime = fonttime.render(self.name + str(time), 1, (255,0,0))
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)

    def draw(self):

        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))

        #ability tab: 
        pygame.draw.rect(screen, (255,246,143),(0 ,0 ,300 , height))

        #primeira abilidade, por enquanto, tackle:
        pygame.draw.rect(screen, (199,97,20),(10,10, 280, 30))
        screen.blit(texttackle,(100,15))
                     #
        
        screen.blit(self.texttime, (300, 10))
        screen.blit(textround, (300, 30))
        for player in players:
            player.draw()
            
        pygame.display.update()

    def receiveevent(self, event):
        for player in players:
            print(player.pos)
            if ((mouseposition[0] - player.pos[0])**2 + (mouseposition[1] - player.pos[1])**2) <= 50**2:
                self.target = player
                roundphase = calculateeffects(self.ability, self.player)

class calculateeffects(object):
    def __init__(self, ability, target):
        self.ability = ability
        self.target = target
        self.name = "calculating effects"
        self.time = 30
        self.time1 = 30
        self.texttime = fonttime.render(self.name + str(self.time), 1, (255,0,0))

    def clock(self):
        #texttime = fonttime.render(self.name + str(time), 1, (255,0,0))
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)

    def draw(self):

        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))

        #ability tab: 
        pygame.draw.rect(screen, (255,246,143),(0 ,0 ,300 , height))

        #primeira abilidade, por enquanto, tackle:
        pygame.draw.rect(screen, (199,97,20),(10,10, 280, 30))
        screen.blit(texttackle,(100,15))
                     #
        
        screen.blit(self.texttime, (300, 10))
        screen.blit(textround, (300, 30))
        for player in players:
            player.draw()
            
        pygame.display.update()

    def effect(self):
        if self.ability == "Tackle":
            self.target.HP -= 1
        
        


class A(object): #A é suposto ser "abilities" mas é para ser mais facil de escrever
    def __init__(self, phase, priority):
        self.phase = phase
        self.priority = priority



def refresh():
    pygame.draw.rect(screen, (0,0,0), (0,0, width, height))

    #ability tab: 
    pygame.draw.rect(screen, (255,246,143),(0 ,0 ,300 , height))

    #primeira abilidade, por enquanto, tackle:
    pygame.draw.rect(screen, (199,97,20),(10,10, 280, 30))
    screen.blit(texttackle,(100,15))
                 #
    
    screen.blit(texttime, (300, 10))
    screen.blit(textround, (300, 30))
    for player in players:
        player.draw()
    pygame.display.update()

def firstdraw():
    pygame.draw.rect(screen, (0,0,0), (0,0, width, height))

    #ability tab:
    pygame.draw.rect(screen, (255,246,143),(0 ,0 ,300 , height))
    pygame.draw.rect(screen, (199,97,20),(10,10, 280, 30))
    
    
    for player in players:
        player.draw()
    pygame.display.update()

def Tackle(target):
    target.HP -= 1

#fonts:
fonttime = pygame.font.SysFont("comicsans", 50, True)
fontA = pygame.font.SysFont("mayence", 30, False, True)

#texts:
texttackle = fontA.render("Tackle", 1, (0,0,0))
textchoosetarget = fonttime.render("choose target(s)!", 1, (255,0,0))


    
craos = player(375, 500, "craos",(255, 0, 255))
player.draw(craos)
#players.append("craos")

robly18 = player(375, 150, "robly18")
player.draw(robly18)
#players.append("robly18")

tavos = player(670,150, "tavos")
player.draw(tavos)

tomis = player(670, 500, "tomis")
player.draw(tomis)


#global time
#time = 30
#global time1
#time1 = 30        
        
BeginningOfRound = True
DuringRound = False
EndOfRound = False

decided = False
roundcount = 1
textround = fonttime.render("round:" + str(roundcount), 1, (0, 0, 255))

firstdraw()

roundphase = chooseability()


#main loop
run = True
while run:
    #if BeginningOfRound and not decided and time >= 0:
     #   texttime = fonttime.render("Beginning Of Round:" + str(time), 1, (255,0,0))
      #  time1 = time1 - 0.1
       # time = math.ceil(time1)
    #else:
     #   BeginningOfRound = False
      #  DuringRound = True
    
    
    #if DuringRound:
     #   BeginningOfRound = True
      #  DuringRound = False
       # roundcount += 1
        #time1 = 30
     #   time = 30
     #   textround = fonttime.render("round:" + str(roundcount), 1, (0, 0, 255))
       # decided = False

    
   # if EndOfRound:
    #    pass


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #nao sei como ver se se clicou no lado esquerdo ou direito do rato... o lado esquerdo é 1 e o lado esquerdo é 3
                
                roundphase.receiveevent(event)
                
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_n: 
                tavos = player(10, 10, "tavos")
                player.draw(tavos)
                
            if event.key == pygame.K_r: 
                a = player(R.randint(0,1000), R.randint(0, 600))
                player.draw(a)
                
            if event.key == pygame.K_t: 
                Tackle(robly18)
                decided = True
                
            if event.key == pygame.K_DELETE:
                run = False
                
    roundphase.clock()
    roundphase.draw()
    #for i in range(10):
     #   pygame.time.delay(10)

    #refresh()
pygame.quit()
