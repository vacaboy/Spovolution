#teste
import random as R
import sys
import pygame

pygame.init()

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((800, 600))
#screen = pygame.display.set_mode((200, 60))


global players
players = []



class player(object):
    def __init__(self,x ,y, name = R.randint(0,999), color = (R.randint(0,255), R.randint(0,255), R.randint(0,255))):
        self.pos = (x, y)
        self.MaxHP = 5
        self.HP = 5
        self.abilities = ["Tackle"]
        self.EXP = 0
        self.stage = 1
        self.color = color
        players.append(str(name))
        
    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, 50)
        pygame.draw.rect(screen, (255,0,0), (self.pos[0]-50, self.pos[1]-60, 100, 10))
        pygame.draw.rect(screen, (0,255,0), (self.pos[0]-50, self.pos[1]-60, round((self.HP/self.MaxHP)*100), 10))
        pygame.display.update()

def refresh():
    craos.draw()
    robly18.draw()
    



def Tackle(target):
    target.HP -= 1




    
craos = player(500, 500, "craos",(255, 0, 255))
player.draw(craos)
#players.append("craos")

robly18 = player(500, 300)
player.draw(robly18)
#players.append("robly18")
print(players)

BeginningOfRound = True
DuringRound = False
EndOfRound = False
time = 30



print(players)

run = True
while run:
   # if BeginningOfRound:
    #    pass


    
    #if DuringRound:
     #   pass


    
   # if EndOfRound:
    #    pass


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == 2: #parece que o event.type de "KEYDOWN" é 2...
            print()
            print(event.key)
            if event.key == 110: #a tecla "n" é o número 110
                tavos = player(10, 10)
                player.draw(tavos)
            if event.key == 114: #a tecla "r" é o numero 114
                a = player(R.randint(0,1000), R.randint(0, 600))
                player.draw(a)
            if event.key == 116: #a tecla "t" é o numero 116
                Tackle(robly18)
    print(robly18.HP)
    pygame.display.update()
    for i in range(10):
        pygame.time.delay(10)


    refresh()
pygame.quit()
