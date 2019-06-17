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



players = []
abilities = []

#__________________________________________________________________________________________________________________________________________________________________________________
class player(object):
    def __init__(self,x ,y, name = "none", color = "none"):
        self.pos = (x, y)
        self.MaxHP = 20
        self.HP = 20
        self.abilities = [ability("Tackle", 1, False, 2), ability("Double Edged Sword", 1, False, 2), ability("ability test", 2, True, 1), ability("Uncertain Footing", 1, False, 3)]
        self.EXP = 0
        self.stage = 1
        self.EXPtoevolve = 30
        self.abilitylastused = " "
        self.abilitylasttarget = " "
        
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
        pygame.draw.circle(screen, self.color, self.pos, 50) #the player
        #HP bar:
        pygame.draw.rect(screen, (255,0,0), (self.pos[0]-50, self.pos[1]-80, 100, 10))
        pygame.draw.rect(screen, (0,255,0), (self.pos[0]-50, self.pos[1]-80, round((self.HP/self.MaxHP)*100), 10))
        textHP = fontHP.render(str(self.HP) + "/" + str(self.MaxHP), 1, (255,0,0))
        screen.blit(textHP, (self.pos[0] + 55, self.pos[1] - 80))
        
        #EXP bar:
        pygame.draw.rect(screen, (0,0,255), (self.pos[0]-50, self.pos[1]-60, round((self.EXP/self.EXPtoevolve)*50), 10))
        pygame.draw.rect(screen, (0,0,255), (self.pos[0]-50, self.pos[1]-60, 100, 10), 1)
        pygame.draw.line(screen, (255,215,0), (self.pos[0],self.pos[1]-60), (self.pos[0],self.pos[1]-50))
        textEXP = fontHP.render(str(self.EXP) + "/" + str(self.EXPtoevolve), 1, (0,0,255))
        screen.blit(textEXP, (self.pos[0] + 55, self.pos[1] - 60))

        #ability last used on:
        textabilitylastused1 = fontHP.render("ability last used:" + " " + self.abilitylastused, 1, self.color)
        textabilitylastused2 = fontHP.render("target:", 1, self.color)
        textabilitylastused3 = fontHP.render(str(self.abilitylasttarget), 1, self.color)
        screen.blit(textabilitylastused1, (self.pos[0] - 55, self.pos[1] + 55))
        screen.blit(textabilitylastused2, (self.pos[0] - 55, self.pos[1] + 65))
        screen.blit(textabilitylastused3, (self.pos[0] - 50, self.pos[1] + 80))
        
        #abilities:
        pygame.draw.rect(screen, (255,246,143),(0 ,0 ,300 , height)) #ability tab
        for ability in self.abilities:
            
            pygame.draw.rect(screen, (199,97,20),(10,(10 + 40 * self.abilities.index(ability)), 280, 30))

            textability = fontA.render(ability.name, 1, (0,0,0))
            
            screen.blit(textability,(30, 15 + 40 * self.abilities.index(ability)))
            
        
        pygame.display.update()

    def drawabilities(self):
        pygame.draw.rect(screen, (255,246,143),(0 ,0 ,300 , height)) #ability tab
        for ability in self.abilities:
            
            pygame.draw.rect(screen, (199,97,20),(10,(10 + 40 * self.abilities.index(ability)), 280, 30))

            textability = fontA.render(ability.name, 1, (0,0,0))
            
            screen.blit(textability,(30, 15 + 40 * self.abilities.index(ability)))
        pygame.display.update()

    def addability(self, ability):
        self.abilities = self.abilities + [ability]
            
#__________________________________________________________________________________________________________________________________________________________________________________
class chooseability(object):
    def __init__(self, caster, roundcount):
        self.roundcount = roundcount
        self.caster = caster
        self.ability = ability("passed", 0, True, 1)
        self.name = "choose ability"
        self.time = 5
        self.time1 = 5
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))

    def clock(self):
        #texttime = fonttime.render(self.name + str(time), 1, (255,0,0))
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)
        if self.time <= 0:
            global roundphase
            roundphase = calculateeffects(self.ability, self.caster, self.roundcount, 0)

    def draw(self):

        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))

        #ability tab: 
        pygame.draw.rect(screen, (255,246,143),(0 ,0 ,300 , height))

        #primeira abilidade, por enquanto, tackle:
        pygame.draw.rect(screen, (199,97,20),(10,10, 280, 30))
        screen.blit(texttackle,(100,15))
                     #
        
        screen.blit(self.texttime, (300, 10))
        screen.blit(self.textround, (300, 30))
        for player in players:
            player.draw()
        craos.drawabilities()
        pygame.display.update()

    def effect(self):
        pass

    

    def receiveevent(self, event):
        global roundphase
        mouseposition = event.pos
        print(mouseposition)
        for i in range(len(craos.abilities)):
            if  10 <= mouseposition[0]  <= 290 and (10 + (40 * i)) <= mouseposition[1] <= (40 + (40 * i)):
                self.ability = craos.abilities[i]
                roundphase = choosetarget(self.ability, self.caster, self.roundcount, self.ability.targetnumber)
            #if 10 <= mouseposition[0]  <= 290 and 10 <= mouseposition[1] <= 40: #clicked in the first ability:
             #   self.ability = "Tackle"
                #Tackle(choosetarget(1)[0])
                #decided = True
              #  roundphase = choosetarget(self.ability, self.caster, self.roundcount)
#__________________________________________________________________________________________________________________________________________________________________________________
class choosetarget(object):
    def __init__(self, ability, caster, roundcount, targetnumber):
        self.roundcount = roundcount
        self.caster = caster
        self.target = []
        self.ability = ability
        self.name = "Choose Target"
        self.time = 30
        self.time1 = 30
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))
        self.targetnumber = targetnumber


    def clock(self):
        #texttime = fonttime.render(self.name + str(time), 1, (255,0,0))
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)
        print(self.ability.name)
        print(str(self.ability.selftarget))

    def draw(self):
        #the screen:
        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))

        #ability tab: 
        pygame.draw.rect(screen, (255,246,143),(0 ,0 ,300 , height))

        #primeira abilidade, por enquanto, tackle:
        pygame.draw.rect(screen, (199,97,20),(10,10, 280, 30))
        screen.blit(texttackle,(100,15))
                     #
        
        screen.blit(self.texttime, (300, 10))
        screen.blit(self.textround, (300, 30))
        for player in players:
            player.draw()
        craos.drawabilities()
        
        pygame.display.update()

    def effect(self):
        global roundphase
        if self.targetnumber == 0:
            roundphase = calculateeffects(self.ability, self.caster, self.target, self.roundcount)

    def receiveevent(self, event):
        mouseposition = event.pos
        for player in players:

            if not self.ability.selftarget:#verify if you can target yourself:
                if player == craos:
                    pass
                else:
                    if ((mouseposition[0] - player.pos[0])**2 + (mouseposition[1] - player.pos[1])**2) <= 50**2:
                        if not player in self.target:
                            self.target.append(player)
                            self.targetnumber -= 1
            else:
                if ((mouseposition[0] - player.pos[0])**2 + (mouseposition[1] - player.pos[1])**2) <= 50**2:
                    if not player in self.target:
                        self.target.append(player)
                        self.targetnumber -= 1
#__________________________________________________________________________________________________________________________________________________________________________________
class calculateeffects(object):
    def __init__(self, ability, caster, target, roundcount):
        self.roundcount = roundcount
        self.caster = caster
        self.ability = ability
        self.target = target
        self.name = "calculating effects"
        self.time = 30
        self.time1 = 30
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))

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
        screen.blit(self.textround, (300, 30))
        for player in players:
            player.draw()
        craos.drawabilities()
        
        pygame.display.update()

    def receiveevent(self, event):
        pass

    def effect(self):
        global roundphase
        global roundcount
        #calcular o que os outros players fazem:
##        for player in players:
##            if player == craos:
##                pass
##            else:
##                a = R.randint(0, len(players)-1)
##                while players[a] == player:
##                    a = R.randint(0, len(players)-1)
##                player.EXP += 1
##                players[a].HP -= 1
##                players[a].EXP += 1
        #até aqui_________________________________

        self.ability.effect(self.target, self.caster)
        roundcount += 1
        roundphase = chooseability(craos, self.roundcount + 1)

        if self.ability == "0":
            roundphase = chooseability(craos, self.roundcount + 1)
            roundcount += 1
    
        

#______________________________________________________________________________________________________________________________________________________________________
class ability(object): 
    def __init__(self, name, targetnumber, selftarget, priority):
        self.name = name
        #self.phase = phase
        self.priority = priority #can be 1, 2 or 3. If it's effects are calculated before, during the batle, or after.
        self.targetnumber = targetnumber # the number of targets the ability has.
        self.selftarget = selftarget # its suposed to be True or False, if the caster can target himself or not.

    def effect(self, targets, caster):
        if self.name == "Tackle":
            caster.abilitylastused = "Tackle"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.EXP += 2
            for target in targets:
                target.EXP += 2
                target.HP -= 2

        elif self.name == "Double Edged Sword":
            caster.abilitylastused = "Double Edged Sword"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.EXP += 5
            caster.HP -= 2
            for target in targets:
                target.EXP += 3
                target.HP -= 3

        elif self.name == "ability test":
            caster.abilitylastused = "ability test"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.EXP = 0
            caster.HP = 0
            for target in targets:
                target.EXP += 3
                target.HP = 10
            
        elif self.name == "Uncertain Footing":
            caster.abilitylastused = "Uncertain Footing"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.EXP = 0
            caster.HP = 0
            for target in targets:
                target.EXP += 3
                target.HP = 10
                
        elif self.name == "passed":
            caster.abilitylastused = "passed"
            caster.abilitylasttarget = []
            pass
            
#______________________________________________________________________________________________________________________________________________________________________

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
fontHP = pygame.font.SysFont("comicsans",20 ,False ,True)

#texts:
texttackle = fontA.render("Tackle", 1, (0,0,0))
textchoosetarget = fonttime.render("choose target(s)!", 1, (255,0,0))
#textround = fonttime.render("round:" + str(roundcount), 1, (0, 0, 255))

    
craos = player(375, 450, "craos",(255, 0, 255))
player.draw(craos)
#players.append("craos")

robly18 = player(375, 150, "robly18")
player.draw(robly18)
#players.append("robly18")

tavos = player(670,150, "tavos")
player.draw(tavos)

tomis = player(670, 450, "tomis")
player.draw(tomis)


BeginningOfRound = True
DuringRound = False
EndOfRound = False

decided = False
roundcount = 1


firstdraw()

roundphase = chooseability(craos, roundcount)

#______________________________________________________________________________________________________________________________________________________________________

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
    roundphase.effect()
    #print(str(roundcount))
    #for i in range(10):
     #   pygame.time.delay(10)

    #refresh()
pygame.quit()
