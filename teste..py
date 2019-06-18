#teste
import random as R
import sys
import pygame
import math

pygame.init()

#width = pygame.display.info()[current_w]
#print(str(width))
width = 1000
height = 600

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((width, height))
#screen = pygame.display.set_mode((200, 60))



players = []
npcs = []
abilities = []
deadcorpses = []

#__________________________________________________________________________________________________________________________________________________________________________________
class player(object):
    def __init__(self,x ,y, name = "none", color = "none"):
        global starterabilities
        self.pos = (x, y)
        self.MaxHP = 20
        self.HP = 20
        self.abilities = []
        self.EXP = 0
        self.stage = 1
        self.EXPtoevolve = 20
        self.abilitylastused = " "
        self.abilitylasttarget = " "
        self.ability = " "
        self.target = []
        self.damaged = False #True or False if this player was damaged this turn or not.
        self.attacksreceived = 0 #keeps track of how many attacks has this player received
        
        if color == "none":
            self.color = (R.randint(0,255), R.randint(0,255), R.randint(0,255))
        else:
            self.color = color
            
        if name == "none":
            self.name = R.randint(0,999)
        else:
            self.name = name
            
        players.append(self)


    def startnewround(self):

        self.damaged = False
        self.target = []
        self.attacksreceived = 0
        if self.HP >self.MaxHP:
            self.HP = self.MaxHP

        
    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, 50) #the player

        #name
        textname = fontHP.render(self.name, 1 , self.color)
        screen.blit(textname, (self.pos[0] + 55, self.pos[1]))
        
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
        textabilitylastused1 = fontHP.render("ability last used:", 1, self.color)
        textabilitylastused2 = fontHP.render("target:", 1, self.color)
        textabilitylastused3 = fontHP.render(str(self.abilitylasttarget), 1, self.color)
        textabilitylastused4 = fontHP.render(self.abilitylastused, 1, self.color)
        screen.blit(textabilitylastused1, (self.pos[0] - 55, self.pos[1] + 55))
        screen.blit(textabilitylastused4, (self.pos[0] - 55, self.pos[1] + 65))
        screen.blit(textabilitylastused2, (self.pos[0] - 55, self.pos[1] + 80))
        screen.blit(textabilitylastused3, (self.pos[0] - 50, self.pos[1] + 95))
        
        #abilities:
##        pygame.draw.rect(screen, (255,246,143),(0 ,0 ,300 , height)) #ability tab
##        for ability in self.abilities:
##            
##            pygame.draw.rect(screen, (199,97,20),(10,(10 + 40 * self.abilities.index(ability)), 280, 30))
##
##            textability = fontA.render(ability.name, 1, (0,0,0))
##            
##            screen.blit(textability,(30, 15 + 40 * self.abilities.index(ability)))
            
        
        #pygame.display.update()

    def drawabilities(self):
        pygame.draw.rect(screen, (255,246,143),(0 ,0 ,300 , height)) #ability tab
        for ability in self.abilities:
            
            pygame.draw.rect(screen, (199,97,20),(10,(10 + 40 * self.abilities.index(ability)), 280, 30))

            textability = fontA.render(ability.name, 1, (0,0,0))
            
            screen.blit(textability,(30, 15 + 40 * self.abilities.index(ability)))
        pygame.display.update()

    def addability(self, ability):
        self.abilities = self.abilities + [ability]
#______________________________________________________________________________________________________________________________________________________________________

class npc(object):
    def __init__(self,x ,y, name = "none", color = "none"):
        global starterabilities
        self.pos = (x, y)
        self.MaxHP = 20
        self.HP = 20
        self.abilities = []
        self.EXP = 0
        self.stage = 1
        self.EXPtoevolve = 30
        self.abilitylastused = " "
        self.abilitylasttarget = " "
        self.ability = " "
        self.target = []
        self.damaged = False #True or False if this player was damaged this turn or not.
        self.attacksreceived = 0 #keeps track of how many attacks has this player received
        
        if color == "none":
            self.color = (R.randint(0,255), R.randint(0,255), R.randint(0,255))
        else:
            self.color = color
            
        if name == "none":
            self.name = R.randint(0,999)
        else:
            self.name = name
            
        players.append(self)
        npcs.append(self)

    def startnewround(self):

        self.damaged = False
        self.target = []
        self.attacksreceived = 0
        if self.HP >self.MaxHP:
            self.HP = self.MaxHP
        

        
    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, 50) #the player

        #name
        textname = fontHP.render(self.name, 1 , self.color)
        screen.blit(textname, (self.pos[0] + 55, self.pos[1]))
        
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
        textabilitylastused1 = fontHP.render("ability last used:", 1, self.color)
        textabilitylastused2 = fontHP.render("target:", 1, self.color)
        textabilitylastused3 = fontHP.render(str(self.abilitylasttarget), 1, self.color)
        textabilitylastused4 = fontHP.render(self.abilitylastused, 1, self.color)
        screen.blit(textabilitylastused1, (self.pos[0] - 55, self.pos[1] + 55))
        screen.blit(textabilitylastused4, (self.pos[0] - 55, self.pos[1] + 65))
        screen.blit(textabilitylastused2, (self.pos[0] - 55, self.pos[1] + 80))
        screen.blit(textabilitylastused3, (self.pos[0] - 50, self.pos[1] + 95))

    def chooseability(self):
        a = R.randint(0, len(self.abilities)-1)
        self.ability = self.abilities[a]

    def choosetarget(self, n, selftarget):
        self.target = []
        while n > 0:
            if selftarget:
                a = R.randint(0, len(players)-1)
                if players[a] in self.target:
                    pass
                else:
                    self.target.append(players[a])
                    n -= 1
            else:
                a = R.randint(0, len(players)-1)
                if (players[a] in self.target) or (players[a] == self):
                    pass
                else:
                    self.target.append(players[a])
                    n -= 1
    
    def addability(self, ability):
        self.abilities = self.abilities + [ability]
#______________________________________________________________________________________________________________________________________________________________________
class deadcorpse(object):
    def __init__(self,x ,y, name, color, HP , MaxHP, abilitylastused, abilitylasttarget, EXP, EXPtoevolve):
        self.pos = (x, y)
        self.name = name
        self.color = color
        self.HP = HP
        self.MaxHP = MaxHP
        self.abilitylastused = abilitylastused
        self.abilitylasttarget = abilitylasttarget
        self. EXP = EXP
        self.EXPtoevolve = EXPtoevolve
        
    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, 50) #the player

        #name
        textname = fontHP.render(self.name, 1 , self.color)
        screen.blit(textname, (self.pos[0] + 55, self.pos[1]))
        
        #HP bar:
        pygame.draw.rect(screen, (255,0,0), (self.pos[0]-50, self.pos[1]-80, 100, 10))
        textHP = fontHP.render(str(self.HP) + "/" + str(self.MaxHP), 1, (255,0,0))
        screen.blit(textHP, (self.pos[0] + 55, self.pos[1] - 80))
        
        #EXP bar:
        pygame.draw.rect(screen, (0,0,255), (self.pos[0]-50, self.pos[1]-60, round((self.EXP/self.EXPtoevolve)*50), 10))
        pygame.draw.rect(screen, (0,0,255), (self.pos[0]-50, self.pos[1]-60, 100, 10), 1)
        pygame.draw.line(screen, (255,215,0), (self.pos[0],self.pos[1]-60), (self.pos[0],self.pos[1]-50))
        textEXP = fontHP.render(str(self.EXP) + "/" + str(self.EXPtoevolve), 1, (0,0,255))
        screen.blit(textEXP, (self.pos[0] + 55, self.pos[1] - 60))

        #ability last used on:
        textabilitylastused1 = fontHP.render("ability last used:", 1, self.color)
        textabilitylastused2 = fontHP.render("target:", 1, self.color)
        textabilitylastused3 = fontHP.render(str(self.abilitylasttarget), 1, self.color)
        textabilitylastused4 = fontHP.render(self.abilitylastused, 1, self.color)
        screen.blit(textabilitylastused1, (self.pos[0] - 55, self.pos[1] + 55))
        screen.blit(textabilitylastused4, (self.pos[0] - 55, self.pos[1] + 65))
        screen.blit(textabilitylastused2, (self.pos[0] - 55, self.pos[1] + 80))
        screen.blit(textabilitylastused3, (self.pos[0] - 50, self.pos[1] + 95))
#__________________________________________________________________________________________________________________________________________________________________________________
class chooseability(object):

    def __init__(self, roundcount):
        self.roundcount = roundcount
        #self.caster = caster
        #self.ability = ability("passed", 0, True, 1)
        self.name = "choose ability"
        self.time = 90
        self.time1 = 90
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))

    def clock(self):
        #texttime = fonttime.render(self.name + str(time), 1, (255,0,0), False)
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)
        if self.time <= 0:
            global roundphase
            craos.ability = ability("passed", 0, True, 1, False)
            roundphase = calculateeffects(self.roundcount)

    def draw(self):

        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))
        craos.drawabilities()
        screen.blit(self.texttime, (300, 10))
        screen.blit(self.textround, (300, 30))
        for player in players:
            player.draw()
        for corpse in deadcorpses:
            corpse.draw()
        pygame.display.update()

    def effect(self):
        
        #verify if the game ended:
        global run
        global height
        for corpse in deadcorpses:
            if corpse.name == "craos":
                textlose = fontend.render("YOU LOST! :( ", 1, (255,0,0))
                screen.blit(textlose, (0, ((height /2) - 100)))
                pygame.display.update()
                pygame.time.delay(5000)
                run = False

        if len(players) == 1 and players[0].name == "craos":
            textwin = fontend.render("YOU WIN! :D ", 1, (0,255,0))
            screen.blit(textwin, (0, ((height /2) - 100)))
            pygame.display.update()
            pygame.time.delay(5000)
            run = False

    

    def receiveevent(self, event):
        global roundphase
        mouseposition = event.pos
        print(mouseposition)
        for i in range(len(craos.abilities)):
            if  10 <= mouseposition[0]  <= 290 and (10 + (40 * i)) <= mouseposition[1] <= (40 + (40 * i)):
                craos.target = []
                craos.ability = craos.abilities[i]
                roundphase = choosetarget(self.roundcount)

#__________________________________________________________________________________________________________________________________________________________________________________
class choosetarget(object):
    def __init__(self, roundcount):
        self.roundcount = roundcount
        #self.caster = caster
        #self.target = []
        #self.ability = ability
        self.name = "Choose Target"
        self.time = 30
        self.time1 = 30
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))
        self.targetnumber = craos.ability.targetnumber


    def clock(self):
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)


    def draw(self):
        #the screen:
        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))
        
        screen.blit(self.texttime, (300, 10))
        screen.blit(self.textround, (300, 30))
        for player in players:
            player.draw()
        for corpse in deadcorpses:
            corpse.draw()
        craos.drawabilities()
        
        pygame.display.update()

    def effect(self):
        global roundphase
        if self.targetnumber == len(players):
            craos.target = players
            roundphase = calculateeffects(self.roundcount)
            
        if (self.targetnumber == (len(players) - 1)) and not craos.ability.selftarget:
            craos.target = npcs
            roundphase = calculateeffects(self.roundcount)
            
        if self.targetnumber <= 0:
            roundphase = calculateeffects(self.roundcount)

    def receiveevent(self, event):
        mouseposition = event.pos
        for player in players:

            if not craos.ability.selftarget:#verify if you can target yourself:
                if (player == craos) or player in craos.target:
                    pass
                else:
                    if ((mouseposition[0] - player.pos[0])**2 + (mouseposition[1] - player.pos[1])**2) <= 50**2:
                        craos.target.append(player)
                        self.targetnumber -= 1
            else:
                if not player in craos.target:
                    if ((mouseposition[0] - player.pos[0])**2 + (mouseposition[1] - player.pos[1])**2) <= 50**2:
                        craos.target.append(player)
                        self.targetnumber -= 1
#__________________________________________________________________________________________________________________________________________________________________________________
class calculateeffects(object):
    def __init__(self, roundcount):
        self.roundcount = roundcount
        #self.caster = caster
        #self.ability = ability
        #self.target = target
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

        
        screen.blit(self.texttime, (300, 10))
        screen.blit(self.textround, (300, 30))
        for player in players:
            player.draw()
        for corpse in deadcorpses:
            corpse.draw()
        craos.drawabilities()
        
        pygame.display.update()

    def receiveevent(self, event):
        pass

    def effect(self):
        global roundphase
        for npc in npcs:
            npc.chooseability()
            npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

        for player in players:
            if player.ability.priority == 1:
                player.ability.effect(player.target, player)

        for player in players: #check if anyone died
            if player.HP <= 0:
                deadcorpses.append(deadcorpse(player.pos[0], player.pos[1], player.name, player.color, player.HP, player.MaxHP, player.abilitylastused, player.abilitylasttarget, player.EXP, player.EXPtoevolve))
                players.remove(player)
        for npc in npcs:
            if npc.HP <=0:
                npcs.remove(npc)
                
        for player in players:
            if player.ability.priority == 2:
                player.ability.effect(player.target, player)

        for player in players: #check if anyone died
            if player.HP <= 0:
                deadcorpses.append(deadcorpse(player.pos[0], player.pos[1], player.name, player.color, player.HP, player.MaxHP, player.abilitylastused, player.abilitylasttarget, player.EXP, player.EXPtoevolve))
                players.remove(player)
        for npc in npcs:
            if npc.HP <=0:
                npcs.remove(npc)
                
        for player in players:
            if player.ability.priority == 3:
                player.ability.effect(player.target, player)
            

        for player in players: #check if anyone died
            if player.HP <= 0:
                deadcorpses.append(deadcorpse(player.pos[0], player.pos[1], player.name, player.color, player.HP, player.MaxHP, player.abilitylastused, player.abilitylasttarget, player.EXP, player.EXPtoevolve))
                players.remove(player)
        for npc in npcs:
            if npc.HP <=0:
                npcs.remove(npc)
                
        for player in players:
            player.startnewround()
                
        roundphase = chooseability(self.roundcount + 1)

    
        

#______________________________________________________________________________________________________________________________________________________________________
class ability(object): 
    def __init__(self, name, targetnumber, selftarget, priority, damage):
        self.name = name
        #self.phase = phase
        self.priority = priority #can be 1, 2 or 3. If it's effects are calculated before, during the batle, or after.
        self.targetnumber = targetnumber # the number of targets the ability has.
        self.selftarget = selftarget # its suposed to be True or False, if the caster can target himself or not.
        self.damage = damage #suposed to be True or False

    def effect(self, targets, caster):
        if self.name == "Tackle":
            caster.abilitylastused = "Tackle"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.EXP += 2
            for target in targets:
                target.EXP += 2
                target.HP -= 2
                target.damaged = True
                target.attacksreceived += 1

        elif self.name == "Double Edged Sword":
            caster.abilitylastused = "Double Edged Sword"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.EXP += 6
            caster.HP -= 2
            for target in targets:
                target.EXP += 4
                target.HP -= 4
                target.damaged = True
                target.attacksreceived += 1

        elif self.name == "Stand Tall":
            caster.abilitylastused = "Stand Tall"
            caster.abilitylasttarget = [player.name for player in targets]
            if caster.attacksreceived >= 2:
                caster.EXP += 7
                for target in targets:
                    target.EXP += 7
                    target.HP -= 7
            
        elif self.name == "Uncertain Footing":
            caster.abilitylastused = "Uncertain Footing"
            caster.abilitylasttarget = [player.name for player in targets]
            if not caster.damaged:
                caster.EXP += 7
                for target in targets:
                    target.EXP += 7
                    target.HP -=7
            else:
                pass
        elif self.name == "QuickPoke":
            caster.abilitylastused = "QuickPoke"
            caster.abilitylasttarget = [player.name for player in targets]
            for target in players:
                if target == caster:
                    pass
                else:
                    target.EXP += 1
                    target.HP -= 1
                    caster.EXP += 1
                    target.damaged = True
                    target.attacksreceived += 1
                
        elif self.name == "chill":
            caster.abilitylastused = "chill"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.HP += 1
                
        elif self.name == "passed":
            caster.abilitylastused = "passed"
            caster.abilitylasttarget = []
            pass
#______________________________________________________________________________________________________________________________________________________________________

#fonts:
fonttime = pygame.font.SysFont("comicsans", 50, True)
fontA = pygame.font.SysFont("mayence", 30, False, True)
fontHP = pygame.font.SysFont("comicsans",20 ,False ,True)
fontend = pygame.font.SysFont("mayence", 180, True)

#texts:
texttackle = fontA.render("Tackle", 1, (0,0,0))
textchoosetarget = fonttime.render("choose target(s)!", 1, (255,0,0))
#textround = fonttime.render("round:" + str(roundcount), 1, (0, 0, 255))

#______________________________________________________________________________________________________________________________________________________________________
#players:
craos = player(375, 450, "craos",(255, 0, 255))
player.draw(craos)


robly18 = npc(375, 150, "robly18")
npc.draw(robly18)


tavos = npc(670,150, "tavos")
npc.draw(tavos)

tomis = npc(670, 450, "tomis")
npc.draw(tomis)

        
#______________________________________________________________________________________________________________________________________________________________________

#abilities:
abilities.append(ability("Tackle", 1, False, 2, True))
abilities.append(ability("Double Edged Sword", 1, False, 2, True))
abilities.append(ability("Uncertain Footing", 1, False, 3, True))
abilities.append(ability("Stand Tall", 1, False, 3, True))
abilities.append(ability("QuickPoke", 0, False, 1, True))
abilities.append(ability("chill", 0, True, 2, False))
starterabilities = abilities


for player in players:
    player.abilities = starterabilities
#______________________________________________________________________________________________________________________________________________________________________


##BeginningOfRound = True
##DuringRound = False
##EndOfRound = False
##
##decided = False
#roundcount = 1



roundphase = chooseability(1)


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
