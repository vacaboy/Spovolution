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



players = [] #has all the plyaer
npcs = [] #has all player except craos. note: "player" and "npc" are different classes

abilities = [[],[],[[],[],[]],[],[]] #keeps track of all abilities in the game, each sublist is the abilities of the correspondend stage. the first sublist are the stage 0 abilities and so on
#the abilities in stage 2 divide into 3 sublists, offensive, defensive and utility
deadcorpses = [] #has all the dead folk
abilityprice = [0, 5, 10] #has the price of each ability for each stage, for stage zero, the price is zero, for stage 1, the price is 5, and so on
evolveprice = [0, 20, 100] #the same but for evolving
evolveHPgain = [0, 75] #HP and MaxHP gained when evolving, per stage.
evolveEXP = [0, 20, 100] #EXP needed to evolve, per stage.
log = [] #isto mantem, ao longo de cada turno, quem da dano a quem.
#__________________________________________________________________________________________________________________________________________________________________________________
class player(object):
    def __init__(self,x ,y, name = "none", color = "none"):
        global starterabilities
        self.pos = (x, y)
        self.MaxHP = 20
        self.HP = 20
        self.abilities = [ability("Tackle",0, 1, False, 2, True, "Offensive"),ability("Double Edged Sword",0, 1, False, 2, True, "Offensive"), ability("chill",0, 0, True, 2, False, "Defensive")]
        self.EXP = 0
        self.stage = 1
        self.EXPtoevolve = 20
        self.abilitylastused = " "
        self.abilitylasttarget = " "
        self.ability = " "
        self.target = []
        self.damaged = False #True or False if this player was damaged this turn or not.
        self.dealtdamage = False #True of False if this player dealt damage this turn or not.
        self.attacksreceived = 0 #keeps track of how many attacks has this player received
        self.conditions = []
        self.unlearnedabilities = []
        self.abilitiesincooldown = []
        self.abilitiesinchannel = []
        
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
        self.dealtdamage = False
        self.target = []
        self.attacksreceived = 0
        if self.HP >self.MaxHP:
            self.HP = self.MaxHP
        for ab in self.abilitiesincooldown:
            ab[1] -= 1
            print(self.name + " has " + ab[0] + " in cooldown for " + str(ab[1]) + " rounds ")
        for ab in self.abilitiesincooldown:
            if ab[1] == 0:
                self.abilitiesincooldown.remove(ab)

        for ab in self.abilitiesinchannel:
            if ab[2] == False or ab[1] == 0:
                print(self.name + " stopped channeling " + ab[0])
                self.abilitiesinchannel.remove(ab)
            else:
                ab[2] = False

        
    def draw(self):
        #the player:
        if self.stage == 1:
            pygame.draw.circle(screen, self.color, self.pos, 50)
        else:
            pygame.draw.rect(screen, self.color, (self.pos[0] - 50, self.pos[1] - 50, 100, 100))
        #name
        textname = fontHP.render(self.name, 1 , self.color)
        screen.blit(textname, (self.pos[0] + 55, self.pos[1]))

        #olhinhos
        pygame.draw.circle(screen, (0,0,0), (self.pos[0]-10, self.pos[1]-30), 5)
        pygame.draw.circle(screen, (0,0,0), (self.pos[0]-10, self.pos[1]-30), 1)
        
        pygame.draw.circle(screen, (0,0,0), (self.pos[0]+10, self.pos[1]-30), 5)
        pygame.draw.circle(screen, (0,0,0), (self.pos[0]+10, self.pos[1]-30), 1)
        
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
        for ab in self.abilities:
            
            pygame.draw.rect(screen, (139,69,19),(10,(10 + 40 * self.abilities.index(ab)), 280, 30))
            if ab.abilitytype == "0": #criar o nome dela:
                textability = fontA.render(ab.name, 1, (0,0,0))
                
            elif ab.abilitytype == "Offensive":
                textability = fontA.render(ab.name, 1, (255,48,48))

            elif ab.abilitytype == "Defensive":
                textability = fontA.render(ab.name, 1, (30,144,255))

            elif ab.abilitytype == "Utility":
                textability = fontA.render(ab.name, 1, (0,201,87))

            screen.blit(textability,(30, 15 + 40 * self.abilities.index(ab)))

            if ab.name in [i[0] for i in self.abilitiesincooldown]:
                pygame.draw.line(screen, (255,0,0), (10, 10 + 40 * self.abilities.index(ab)), (290, 40 + 40 * self.abilities.index(ab)) )
                pygame.draw.line(screen, (255,0,0), (10, 40 + 40 * self.abilities.index(ab)), (290, 10 + 40 * self.abilities.index(ab)) )

    def addability(self, ability):
        self.abilities = self.abilities + [ability]
#______________________________________________________________________________________________________________________________________________________________________

class npc(object):
    def __init__(self,x ,y, name = "none", color = "none"):
        global starterabilities
        self.pos = (x, y)
        self.MaxHP = 20
        self.HP = 20
        #self.abilities = [ability("Tackle",0, 1, False, 2, True, "Offensive"), ability("Limitless",2, 0,True, 3, False, "Utility")]
        self.abilities = [ability("Tackle",0, 1, False, 2, True, "Offensive"), ability("Double Edged Sword",0, 1, False, 2, True, "Offensive"), ability("chill",0, 0, True, 2, False, "Defensive")]
        self.EXP = 0
        self.stage = 1
        self.EXPtoevolve = 20
        self.abilitylastused = " "
        self.abilitylasttarget = " "
        self.ability = " "
        self.target = []
        self.damaged = False #True or False if this player was damaged this turn or not.
        self.dealtdamage = False #True of False if this player dealt damage this turn or not.
        self.attacksreceived = 0 #keeps track of how many attacks has this player received
        self.conditions = []
        self.unlearnedabilities = []
        self.abilitiesincooldown = []
        self.abilitiesinchannel = []
        
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
        self.dealtdamage = False
        self.target = []
        self.attacksreceived = 0
        if self.HP >self.MaxHP:
            self.HP = self.MaxHP
        for ab in self.abilitiesincooldown:
            ab[1] -= 1
            print(self.name + " has " + ab[0] + " in cooldown for " + str(ab[1]) + " rounds ")
        for ab in self.abilitiesincooldown:
            if ab[1] == 0:
                self.abilitiesincooldown.remove(ab)

        for ab in self.abilitiesinchannel:
            if ab[2] == False or ab[1] == 0:
                print(self.name + " stopped channeling " + ab[0])
                self.abilitiesinchannel.remove(ab)
            else:
                ab[2] = False
        

        
    def draw(self):
        #the player:
        if self.stage == 1:
            pygame.draw.circle(screen, self.color, self.pos, 50)
        else:
            pygame.draw.rect(screen, self.color, (self.pos[0] - 50, self.pos[1] - 50, 100, 100))

        #name
        textname = fontHP.render(self.name, 1 , self.color)
        screen.blit(textname, (self.pos[0] + 55, self.pos[1]))

        #olhinhos
        pygame.draw.circle(screen, (0,0,0), (self.pos[0]-10, self.pos[1]-30), 5)
        pygame.draw.circle(screen, (0,0,0), (self.pos[0]-10, self.pos[1]-30), 1)
        
        pygame.draw.circle(screen, (0,0,0), (self.pos[0]+10, self.pos[1]-30), 5)
        pygame.draw.circle(screen, (0,0,0), (self.pos[0]+10, self.pos[1]-30), 1)
        
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
        a = True
        while a:
            b = R.randint(0, len(self.abilities)-1)
            if not (self.abilities[b].name in [i[0] for i in self.abilitiesincooldown]):
                self.ability = self.abilities[b]
                a = False

    def choosetarget(self, n, selftarget):
        self.target = []
        if selftarget: #se te podes dar target a ti mesmo
            if n >= len(players): #se o numero targets for maior ou igual que o numero de players, entao os targets sao todos os players:
                for p in players:
                    self.target.append(p)
            else:
                while n > 0: #se nao, vamos escolher players
                    a = R.randint(0, len(players)-1)
                    if players[a] in self.target:
                        pass
                    else:
                        self.target.append(players[a])
                        n -= 1
        else:#se nao de podes dar target a ti mesmo...
            if n >= (len(players) - 1): #entao se o numero de targets for maior ou igual que o numero de players - 1, entao os targets sao todos os inimigos
                for p in players:
                    if p == self:
                        pass
                    else:
                        self.target.append(p)
            else:
                while n > 0:#se nao, vamos escolher inimigos
                    a = R.randint(0, len(players)-1)
                    if (players[a] in self.target) or (players[a] == self):
                        pass
                    else:
                        self.target.append(players[a])
                        n -= 1
        if self.ability.channel > 0: #se a habilidade escolhida tem channel:
            if self.ability.name in [i[0] for i in self.abilitiesinchannel]: #se o player ja esta a dar channel à habilidade
                a = [i[0] == self.ability.name for i in self.abilitiesinchannel].index(True)
                if self.abilitiesinchannel[a][1] > 1: #se a habilidade nao vai atuar este turno
                    self.target = []
            elif not (self.ability.name in [i[0] for i in self.abilitiesinchannel]): #se o player ainda nao esta a dar channel à habilidade:
                self.target = []
       
    
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

        #dead
        textdead = fontHP.render("R.I.P", 1, (0,0,0))
        screen.blit(textdead, (self.pos[0] - 10, self.pos[1] - 10))

        #olhinhos
        pygame.draw.circle(screen, (0,0,0), (self.pos[0]-10, self.pos[1]-30), 5)
        pygame.draw.circle(screen, (0,0,0), (self.pos[0]-10, self.pos[1]-30), 1)
        
        pygame.draw.circle(screen, (0,0,0), (self.pos[0]+10, self.pos[1]-30), 5)
        pygame.draw.circle(screen, (0,0,0), (self.pos[0]+10, self.pos[1]-30), 1)

        
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

    def __init__(self, roundcount, time = 900):
        self.roundcount = roundcount
        self.name = "choose ability"
        self.time = time
        self.time1 = time
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))
        self.textgainability = fontA.render("learn ability", 1, (0,0,0))
        self.textevolve = fontA.render("EVOLVE!", 1, (0,0,0))
        self.textunlearnability = fontA.render("Unlearn ability", 1, (0,0,0))

    def clock(self):
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)
        if self.time <= 0:
            global roundphase
            craos.ability = ability("passed",3, 0, True, 1, False)
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

        #escolha de habilidade ou evoluir ou desaprender:
        pygame.draw.rect(screen, (227,207,87), (320, 290, 160, 30))
        pygame.draw.rect(screen, (227,207,87), (520, 290, 160, 30))
        pygame.draw.rect(screen, (227,207,87), (720, 290, 160, 30))

        screen.blit(self.textgainability, (330, 295))
        screen.blit(self.textevolve, (530, 295))
        screen.blit(self.textunlearnability, (730, 295))
        
        pygame.display.update()

    def effect(self):
        pass

        

    

    def receiveevent(self, event):
        global roundphase
        mouseposition = event.pos
        print(mouseposition)
        #escolher habilidade
        for i in range(len(craos.abilities)):
            if  10 <= mouseposition[0]  <= 290 and (10 + (40 * i)) <= mouseposition[1] <= (40 + (40 * i)):
                #if craos.abilities[i].cooldown == 0:
                #só podes escolher se a habilidade nao estiver em cooldown
                if not(craos.abilities[i].name in [j[0] for j in craos.abilitiesincooldown]):
                    craos.target = []
                    craos.ability = craos.abilities[i]
                    for npc in npcs:#npc's tambem escolhem as habilidades
                        npc.chooseability()

                    for player in players:#fazer os efeitos que atuam agora
                        for condition in player.conditions:
                            if condition.priority == "chooseability":
                                condition.effect()
                    roundphase = choosetarget(self.roundcount)
                else:
                    print("this ability is in cooldown")# for" " + str(craos.abilitiesincooldown[i]) + " turns.")

        #ganhar habilidade
        if 320 <= mouseposition[0] <= 480 and 290 <= mouseposition[1] <= 320:
            print("ganhar habilidade")
            if craos.EXP < abilityprice[craos.stage]:
                print("not enough EXP")
            else:
                if craos.stage == 1:
                    self.gainability(craos)
                elif craos.stage == 2:
                    roundphase = gainability2(self.roundcount, self.time)
        #evoluir            
        elif 520 <= mouseposition[0] <= 680 and 290 <= mouseposition[1] <= 320:
            print("evoluir")
            self.evolve(craos)
        #desaprender habilidade:
        elif 720 <= mouseposition[0] <= 880 and 290 <= mouseposition[1] <= 320:
            print("desaprender habilidade")
            roundphase = loseability(self.roundcount, self.time)

    def gainability(self, player):
        #verify if the player already has all the abilities:
        a = True
        stageabilities = abilities[player.stage]
        for ab in stageabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        #verify if the player has enough EXP:
        elif player.EXP < abilityprice[player.stage]:
            pass
        else:
            while not a:
                b = R.randint(0,len(stageabilities) - 1)
                #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                if (not (stageabilities[b].name in [i.name for i in player.abilities])) and ( not (stageabilities[b].name in [i.name for i in player.unlearnedabilities])):
                #if not (stageabilities[b].name in [i.name for i in player.abilities]):
                
                    player.abilities.append(stageabilities[b].clone())
                    a = True
                    player.EXP -= abilityprice[player.stage]

    def gainabilityforfree(self, player):
        #verify if the player already has all the abilities:
        a = True
        stageabilities = abilities[player.stage]
        for ab in stageabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        else:
            while not a:
                b = R.randint(0,len(stageabilities) - 1)
                print()
                print(b)
                print()
                #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                if (not (stageabilities[b].name in [i.name for i in player.abilities])) and ( not (stageabilities[b].name in [i.name for i in player.unlearnedabilities])):
                #if not (stageabilities[b].name in [i.name for i in player.abilities]):
                    player.abilities.append(stageabilities[b].clone())
                    a = True
                  

    def evolve(self, player):
        global roundphase
        #verify if the player has enough EXP:
        if player.EXP < evolveprice[player.stage]:
            print("Not enought EXP")
        elif player.stage == 2:
            print("ainda nao esta implementado evoluires mais :(")
        else:
            player.EXP -= evolveprice[player.stage]
            player.HP += evolveHPgain[player.stage]
            player.MaxHP += evolveHPgain[player.stage]
            player.EXPtoevolve = evolveEXP[player.stage + 1]
            player.stage += 1
            roundphase = evolve1(self.roundcount, self.time)


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

        if self.targetnumber <= 0: #se ja estao os targets todos escolhidos, siga em frente
            
            for npc in npcs: #escolher target dos npcs
                npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

            for player in players: #condiçoes que atuam agora:
                for condition in player.conditions:
                    if condition.priority == "after choosetarget":
                        condition.effect()
                        
            roundphase = calculateeffects(self.roundcount)
            
        #se a habilidade escolhida é de channel, e não vai fazer o efeito este turno, siga a marinha
        if craos.ability.channel > 0:#se a habilidade escolhida tem channel:
            if craos.ability.name in [i[0] for i in craos.abilitiesinchannel]: #se o player ja esta a dar channel à habilidade
                a = [i[0] == craos.ability.name for i in craos.abilitiesinchannel].index(True)
                print(str(craos.abilitiesinchannel[a]))
                if craos.abilitiesinchannel[a][1] >= 2: #se a habilidade nao vai atuar este turno
                    for npc in npcs: #escolher target dos npcs
                        npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

                    for player in players: #condiçoes que atuam agora:
                        for condition in player.conditions:
                            if condition.priority == "after choosetarget":
                                condition.effect()
                        
                    roundphase = calculateeffects(self.roundcount)
                else:
                    if ((self.targetnumber >= (len(players) - 1)) and not craos.ability.selftarget): #se a habilidade tem toda a gente como target, siga
                        for p in npcs:    
                            craos.target.append(p)
                        for npc in npcs:#escolher o target dos npcs
                            npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

                        for player in players: #condiçoes que atuam agora:
                            for condition in player.conditions:
                                if condition.priority == "after choosetarget":
                                    condition.effect()
                          
                        roundphase = calculateeffects(self.roundcount)
                        
                    elif self.targetnumber >= len(players):
                        for p in players:    
                            craos.target.append(p)
                        for npc in npcs:#escolher o target dos npcs
                            npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

                        for player in players: #condiçoes que atuam agora:
                            for condition in player.conditions:
                                if condition.priority == "after choosetarget":
                                    condition.effect()
                          
                        roundphase = calculateeffects(self.roundcount)

                    
                    
            elif not (craos.ability.name in [i[0] for i in craos.abilitiesinchannel]): #se o player ainda nao esta a dar channel à habilidade:
                for npc in npcs: #escolher target dos npcs
                    npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

                for player in players: #condiçoes que atuam agora:
                    for condition in player.conditions:
                        if condition.priority == "after choosetarget":
                            condition.effect()
                            
                roundphase = calculateeffects(self.roundcount)
            
                
        elif ((self.targetnumber >= (len(players) - 1)) and not craos.ability.selftarget): #se a habilidade tem toda a gente como target, siga
            for p in npcs:    
                craos.target.append(p)
            
            for npc in npcs:#escolher o target dos npcs
                npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

            for player in players: #condiçoes que atuam agora:
                for condition in player.conditions:
                    if condition.priority == "after choosetarget":
                        condition.effect()
              
            roundphase = calculateeffects(self.roundcount)

        elif self.targetnumber >= len(players): #se a habilidade tem toda a gente como target, siga
            for p in players:    
                craos.target.append(p)
            
            for npc in npcs:#escolher o target dos npcs
                npc.choosetarget(npc.ability.targetnumber, npc.ability.selftarget)

            for player in players: #condiçoes que atuam agora:
                for condition in player.conditions:
                    if condition.priority == "after choosetarget":
                        condition.effect()
              
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
        #phase 1 of combat:
        for player in players:#effects of priority 1 abilities
            if player.ability.priority == 1:
                player.ability.effect(player.target, player)
                
            for condition in player.conditions: #conditions with priority 1
                if condition.priority == 1:
                    condition.effect()

        for player in players: #check if anyone died
            if player.HP <= 0:
                deadcorpses.append(deadcorpse(player.pos[0], player.pos[1], player.name, player.color, player.HP, player.MaxHP, player.abilitylastused, player.abilitylasttarget, player.EXP, player.EXPtoevolve))
                players.remove(player)
        for npc in npcs:
            if npc.HP <=0:
                npcs.remove(npc)




        
        #phase 2 of combat:     
        for player in players:#effects of priority 2 abilities
            if player.ability.priority == 2:
                player.ability.effect(player.target, player)
                
            for condition in player.conditions: #conditions of priority 2
                if condition.priority == 2:
                    condition.effect()

        for player in players: #check if anyone died
            if player.HP <= 0:
                deadcorpses.append(deadcorpse(player.pos[0], player.pos[1], player.name, player.color, player.HP, player.MaxHP, player.abilitylastused, player.abilitylasttarget, player.EXP, player.EXPtoevolve))
                players.remove(player)
        for npc in npcs:
            if npc.HP <=0:
                npcs.remove(npc)
        


        #phase 3 of combat    
        for player in players:#effects of priority 3 abilities
            if player.ability.priority == 3:
                player.ability.effect(player.target, player)

            for condition in player.conditions: #conditions of priority 3
                if condition.priority == 3:
                    condition.effect()
            

        for player in players: #check if anyone died
            if player.HP <= 0:
                deadcorpses.append(deadcorpse(player.pos[0], player.pos[1], player.name, player.color, player.HP, player.MaxHP, player.abilitylastused, player.abilitylasttarget, player.EXP, player.EXPtoevolve))
                if player.name in [i.name for i in npcs]:
                    players.remove(player)
                    npcs.remove(player)
                else:
                    players.remove(player)
##        for npc in npcs:
##            if npc.HP <=0:
##                npcs.remove(npc)

        #phase 4 of combat    
        for player in players:#effects of priority 4 abilities
            if player.ability.priority == 4:
                player.ability.effect(player.target, player)

            for condition in player.conditions: #conditions of priority 4
                if condition.priority == 4:
                    condition.effect()
            

        for player in players: #check if anyone died
            if player.HP <= 0:
                deadcorpses.append(deadcorpse(player.pos[0], player.pos[1], player.name, player.color, player.HP, player.MaxHP, player.abilitylastused, player.abilitylasttarget, player.EXP, player.EXPtoevolve))
                if player.name in [i.name for i in npcs]:
                    players.remove(player)
                    npcs.remove(player)
                else:
                    players.remove(player)
                
        for player in players:
            player.startnewround()

        #verify if the game ended:
        self.draw()
        
        global run
        global height
        global log
        if len(players) == 0:
            texttie = fontend.render("Its a Tie! :|", 1 ,(255,193,37))
            screenblit(texttie, (0, ((height / 2) - 100)))
            pygame.display.update()
            pygame.time.delay(5000)
            run = False
        else:
            for corpse in deadcorpses:
                if corpse.name == "craos":
                    textlose = fontend.render("LOSER! :( ", 1, (255,0,0))
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

        #level up the npc's
        if craos.stage == 2:
            for npc in npcs:
                if npc.stage == 1:
                    if npc.EXP >=evolveprice[npc.stage]:
                        npc.EXP -= evolveprice[npc.stage]
                        npc.HP += evolveHPgain[npc.stage]
                        npc.MaxHP += evolveHPgain[npc.stage]
                        npc.EXPtoevolve = evolveEXP[npc.stage + 1]
                        npc.stage += 1
                        npc.abilities = []
                        self.gainabilityoffensive(npc)
                        self.gainabilityoffensive(npc)
                        self.gainabilitydefensive(npc)

        log = []
        
        roundphase = chooseability(self.roundcount + 1)
        print()
        print("round: " + str(self.roundcount + 1))



    def gainabilityoffensive(self, player):
        a = True
        offensiveabilities = abilities[2][0]
        while a:
            b = R.randint(0,len(offensiveabilities) - 1)
            #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
            if not (offensiveabilities[b].name in [i.name for i in player.abilities]):
                player.abilities.append(offensiveabilities[b].clone())
                a = False

    def gainabilitydefensive(self, player):
        a = True
        defensiveabilities = abilities[2][1]
        while a:
            b = R.randint(0,len(defensiveabilities) - 1)
            #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
            if not (defensiveabilities[b].name in [i.name for i in player.abilities]):
                player.abilities.append(defensiveabilities[b].clone())
                a = False


    def gainabilityutility(self, player):
        a = True
        utilityabilities = abilities[2][2]
        while a:
            b = R.randint(0,len(utilityabilities) - 1)
            #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
            if not (utilityabilities[b].name in [i.name for i in player.abilities]):
                player.abilities.append(utilityabilities[b].clone())
                a = False

#_____________________________________________________________________________________________________________________________________________________________________
class loseability(object):

    def __init__(self, roundcount, time = 30):
        self.roundcount = roundcount
        self.name = "Choose ability to unlearn"
        self.time = time
        self.time1 = time
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))
        self.textreturn = fontA.render("Return", 1, (0,0,0))
        
    def clock(self):
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)
        if self.time <= 0:
            global roundphase
            roundphase = chooseability(self.roundcount)

    def draw(self):

        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))
        craos.drawabilities()
        screen.blit(self.texttime, (300, 10))
        screen.blit(self.textround, (300, 30))
        for player in players:
            player.draw()
        for corpse in deadcorpses:
            corpse.draw()
        #return option:
        pygame.draw.rect(screen, (227,207,87), (320, 290, 160, 30))
        screen.blit(self.textreturn, (330, 295))
        
        pygame.display.update()

    def effect(self):
        pass

    

    def receiveevent(self, event):
        global roundphase
        mouseposition = event.pos
        print(mouseposition)

        for i in range(len(craos.abilities)):
            if  10 <= mouseposition[0]  <= 290 and (10 + (40 * i)) <= mouseposition[1] <= (40 + (40 * i)):
                craos.unlearnedabilities.append(craos.abilities[i])
                craos.abilities.remove(craos.abilities[i])
                roundphase = chooseability(self.roundcount, self.time + 5)
            if  320 <= mouseposition[0] <= 480 and 290 <= mouseposition[1] <= 320: #return button
                roundphase = chooseability(self.roundcount, self.time + 5)

#_____________________________________________________________________________________________________________________________________________________________________
class evolve1(object):

    def __init__(self, roundcount, time = 30):
        self.roundcount = roundcount
        self.name = "You are Evolving!"
        self.time = time
        self.time1 = time
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))
        self.textoffensive = fontA.render("Offensive", 1, (0,0,0))
        self.textdefensive = fontA.render("Defensive", 1, (0,0,0))
        self.textutility = fontA.render("Utility", 1, (0,0,0))
        self.number = 3 #abilities he gets to choose
        
    def clock(self):
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)
        if self.time <= 0:
            global roundphase
            roundphase = chooseability(self.roundcount)

    def draw(self):

        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))
        craos.drawabilities()
        screen.blit(self.texttime, (300, 10))
        screen.blit(self.textround, (300, 30))
        for player in players:
            player.draw()
        for corpse in deadcorpses:
            corpse.draw()

        if craos.stage == 2:
            #escolha de tipo de habilidade :
            pygame.draw.rect(screen, (255,48,48), (320, 290, 160, 30))
            pygame.draw.rect(screen, (30,144,255), (520, 290, 160, 30))
            pygame.draw.rect(screen, (0,201,87), (720, 290, 160, 30))


            screen.blit(self.textoffensive, (330, 295))
            screen.blit(self.textdefensive, (530, 295))
            screen.blit(self.textutility, (730, 295))
        
        pygame.display.update()

    def effect(self):
        global roundphase
        if self.number <= 0:
            for npc in npcs:
                if npc.EXP >=evolveprice[npc.stage]:
                    npc.EXP -= evolveprice[npc.stage]
                    npc.HP += evolveHPgain[npc.stage]
                    npc.MaxHP += evolveHPgain[npc.stage]
                    npc.EXPtoevolve = evolveEXP[npc.stage + 1]
                    npc.stage += 1
                    npc.abilities = []
                    self.gainabilityoffensive(npc)
                    self.gainabilityoffensive(npc)
                    self.gainabilitydefensive(npc)
            
            roundphase = chooseability(self.roundcount, self.time + 15)


    

    def receiveevent(self, event):
        global roundphase
        mouseposition = event.pos
        print(mouseposition)
        if  320 <= mouseposition[0]  <= 480 and 290 <= mouseposition[1] <= 320:
            self.gainabilityoffensive(craos)
            self.number -= 1
        elif  520 <= mouseposition[0]  <= 680 and 290 <= mouseposition[1] <= 320:
            self.gainabilitydefensive(craos)
            self.number -= 1
        elif  720 <= mouseposition[0]  <= 880 and 290 <= mouseposition[1] <= 320:
            self.gainabilityutility(craos)
            self.number -= 1

    def gainabilityoffensive(self, player):
        a = True
        offensiveabilities = abilities[2][0]
        while a:
            b = R.randint(0,len(offensiveabilities) - 1)
            #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
            if not (offensiveabilities[b].name in [i.name for i in player.abilities]):
                player.abilities.append(offensiveabilities[b].clone())
                a = False

    def gainabilitydefensive(self, player):
        a = True
        defensiveabilities = abilities[2][1]
        while a:
            b = R.randint(0,len(defensiveabilities) - 1)
            #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
            if not (defensiveabilities[b].name in [i.name for i in player.abilities]):
                player.abilities.append(defensiveabilities[b].clone())
                a = False


    def gainabilityutility(self, player):
        a = True
        utilityabilities = abilities[2][2]
        while a:
            b = R.randint(0,len(utilityabilities) - 1)
            #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
            if not (utilityabilities[b].name in [i.name for i in player.abilities]):
                player.abilities.append(utilityabilities[b].clone())
                a = False

#_____________________________________________________________________________________________________________________________________________________________________
class gainability2(object):

    def __init__(self, roundcount, time = 30):
        self.roundcount = roundcount
        self.name = "choose ability type"
        self.time = time
        self.time1 = time
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        self.textround = fonttime.render("round:" + str(self.roundcount), 1, (0, 0, 255))
        self.textoffensive = fontA.render("Offensive", 1, (0,0,0))
        self.textdefensive = fontA.render("Defensive", 1, (0,0,0))
        self.textutility = fontA.render("Utility", 1, (0,0,0))
        
    def clock(self):
        self.time1 = self.time1 - 0.1
        self.time = math.ceil(self.time1)
        self.texttime = fonttime.render(self.name + ":" + str(self.time), 1, (255,0,0))
        for i in range(10):
            pygame.time.delay(10)
        if self.time <= 0:
            global roundphase
            roundphase = chooseability(self.roundcount, self.time)

    def draw(self):

        pygame.draw.rect(screen, (0,0,0), (0,0, width, height))
        craos.drawabilities()
        screen.blit(self.texttime, (300, 10))
        screen.blit(self.textround, (300, 30))
        for player in players:
            player.draw()
        for corpse in deadcorpses:
            corpse.draw()

        if craos.stage == 2:
            #escolha de tipo de habilidade :
            pygame.draw.rect(screen, (255,48,48), (320, 290, 160, 30))
            pygame.draw.rect(screen, (30,144,255), (520, 290, 160, 30))
            pygame.draw.rect(screen, (0,201,87), (720, 290, 160, 30))
    ##        pygame.draw.rect(screen, (227,207,87), (490, 295, 20, 20))
    ##        pygame.draw.line(screen, (255,0,0),(490, 295) , (510, 315))
    ##        pygame.draw.line(screen, (255,0,0),(510, 295) , (490, 315))

            screen.blit(self.textoffensive, (330, 295))
            screen.blit(self.textdefensive, (530, 295))
            screen.blit(self.textutility, (730, 295))
        
        pygame.display.update()

    def effect(self):
        pass


    

    def receiveevent(self, event):
        global roundphase
        mouseposition = event.pos
        print(mouseposition)
        if  320 <= mouseposition[0]  <= 480 and 290 <= mouseposition[1] <= 320:
            self.gainabilityoffensive(craos)
            roundphase = chooseability(self.roundcount, self.time)
        elif  520 <= mouseposition[0]  <= 680 and 290 <= mouseposition[1] <= 320:
            self.gainabilitydefensive(craos)
            roundphase = chooseability(self.roundcount, self.time)
        elif  720 <= mouseposition[0]  <= 880 and 290 <= mouseposition[1] <= 320:
            self.gainabilityutility(craos)
            roundphase = chooseability(self.roundcount, self.time)

    def gainabilityoffensive(self, player):
        #verify if the player already has all the abilities:
        a = True
        offensiveabilities = abilities[player.stage][0] #a list of the offensive abilities of the second stage
        for ab in offensiveabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        #verify if the player has enough EXP:
        elif player.EXP < abilityprice[player.stage]:
            pass
        else:
            while not a:
                b = R.randint(0,len(offensiveabilities) - 1)
                #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                if (not (offensiveabilities[b].name in [i.name for i in player.abilities])) and ( not (offensiveabilities[b].name in [i.name for i in player.unlearnedabilities])): 
                    player.abilities.append(offensiveabilities[b].clone())
                    a = True
                    player.EXP -= abilityprice[player.stage]

    def gainabilitydefensive(self, player):
        #verify if the player already has all the abilities:
        a = True
        defensiveabilities = abilities[player.stage][1]
        for ab in defensiveabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        #verify if the player has enough EXP:
        elif player.EXP < abilityprice[player.stage]:
            pass
        else:
            while not a:
                b = R.randint(0,len(defensiveabilities) - 1)
                #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                if (not (defensiveabilities[b].name in [i.name for i in player.abilities])) and ( not (defensiveabilities[b].name in [i.name for i in player.unlearnedabilities])):
                #if not (defensiveabilities[b].name in [i.name for i in player.abilities]):
                    player.abilities.append(defensiveabilities[b].clone())
                    a = True
                    player.EXP -= abilityprice[player.stage]
                    
    def gainabilityutility(self, player):
        #verify if the player already has all the abilities:
        a = True
        utilityabilities = abilities[player.stage][2]
        for ab in utilityabilities:
            if (not (ab.name in [i.name for i in player.abilities])) and (not (ab.name in [i.name for i in player.unlearnedabilities])):
                a = False
        if a:
            pass
        #verify if the player has enough EXP:
        elif player.EXP < abilityprice[player.stage]:
            pass
        else:
            while not a:
                b = R.randint(0,len(utilityabilities) - 1)
                #verificar se o nome da habilidade não está nos nomes das habilidades do jogador
                if (not (utilityabilities[b].name in [i.name for i in player.abilities])) and ( not (utilityabilities[b].name in [i.name for i in player.unlearnedabilities])):
                #if not (utilityabilities[b].name in [i.name for i in player.abilities]):
                    player.abilities.append(utilityabilities[b].clone())
                    a = True
                    player.EXP -= abilityprice[player.stage]
#_______________________________________________________________________________________________________________________________________________________________________
class condition(object):
    def __init__(self, name, target, priority, duration):
        self.name = name
        self.target = target
        self.priority = priority
        self.duration = duration

    def effect(self):
        global log
        if self.name == "teste":
            self.duration -= 1
            if self.target.ability.damage:
                print("dás mais 3 de dano")
                for target in self.target.target:
                    target.HP -=3
                    self.target.EXP += 3
        
        elif self.name == "Paralyzed":
            print(self.target.name + " is paralyzed this round")
            self.target.ability = ability("passed", 3, 0, True, 1, False)
            self.duration -= 1

        elif self.name == "Rock Solid":
            print("because of Rock Solid, " + str(self.target.name) + " took no damage")
            for player in players:
                if player == self.target:
                    pass
                else:
                    if player.ability.damage and (self.target in player.target): #se a habilidade der target ao caster E se a habilidade der dano, entao retira o caster dos targets.
                        player.target.remove(self.target)
            self.duration -= 1

        elif self.name == "Regenerate":
            print(self.target.name + " regenerates 3 HP")
            self.target.HP += 3
            self.duration -= 1

        elif self.name == "Fight Stance":
            self.duration -= 1
            if self.target.ability.damage and self.target.ability.worked:
                for target in self.target.target:
                    target.HP -= 7 
                    self.target.EXP += 7
                    target.EXP += 7
                    print(self.target.name + " dealt 7 more damage")

        elif self.name == "Limitless":
            self.duration -= 1
            for i in log:
                if i[0] == self.target:
                    i[2].HP -= i[1]
                    i[2].EXP += i[1]
                    self.target.EXP += i[1]
                    print(self.target.name + " dealt " + str(i[1]) + " extra damage because of Limiless")

        elif self.name == "Asleep":
            
            a = R.randint(1,100)
            print("coisas de sleep:")
            print(str(a))
            print(str(self.duration))
            if self.duration == 5 and a <= 30:
                self.duration = 1
            elif self.duration == 4 and a <= 50:
                self.duration = 1
            elif self.duration == 3 and a <= 70:
                self.duration = 1
            elif self.duration == 2 and a <= 80:
                self.duration = 1
            elif self.duration == 1 and a <= 90:
                self.duration = 1
            else:
                self.target.ability = ability("passed", 3, 0, True, 1, False)
                print(self.target.name + " is Asleep this round")
            self.duration -= 1

        elif self.name == "Intimidated":
            self.duration -= 1
            if self.target.ability.damage and self.target.ability.worked:
                for i in log:
                    if i[0] == self.target:
                        a = 5
                        if i[1] < 5:
                            a = i[i]
                        i[2].HP += a 
                        self.target.EXP -= a
                        i[2].EXP -= a
                        print(self.target.name + " dealt minus " + str(a) + " damage")
                



        if self.duration == 0:
            if self.name == "Asleep":
                print(self.target.name + " Woke UP!")
            self.target.conditions.remove(self)
            
            

#______________________________________________________________________________________________________________________________________________________________________
class ability(object): 
    def __init__(self, name, phase, targetnumber, selftarget, priority, damage, abilitytype = "0", worked = False, cooldown = 0, channel = 0):
        self.name = name
        self.phase = phase
        self.priority = priority #can be 1, 2 or 3. If it's effects are calculated before, during the batle, or after.
        self.targetnumber = targetnumber # the number of targets the ability has.
        self.selftarget = selftarget # its suposed to be True or False, if the caster can target himself or not.
        self.damage = damage #suposed to be True or False
        self.abilitytype = abilitytype
        self.worked = worked
        self.cooldown = cooldown
        self.channel = channel
##    def startnewround(self):
##        self.worked = False
##        if self.cooldown >= 1:
##            self.cooldown -= 1
##            print(self.name + str(self.cooldown))

    def clone(self):
        print(self.name)
        return ability(self.name, self.phase, self.targetnumber, self.selftarget, self.priority, self.damage, self.abilitytype, self.worked, self.cooldown, self.channel)


        
    def effect(self, targets, caster):
        global log
        if self.name == "Tackle":
            caster.abilitylastused = "Tackle"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.dealtdamage = True
            for target in targets:
                log.append([caster, 2, target])
                caster.EXP += 2
                target.EXP += 2
                target.HP -= 2
                target.damaged = True
                target.attacksreceived += 1
                self.worked = True
                print(caster.name + " dealt 2 damage to " + target.name + " using tackle")

        elif self.name == "Double Edged Sword":
            caster.abilitylastused = "Double Edged Sword"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.dealtdamage = True
            for target in targets:
                log.append([caster, 3, target])
                log.append([caster, 2, caster])
                caster.EXP += 5
                caster.HP -= 2
                target.EXP += 3
                target.HP -= 3
                target.damaged = True
                target.attacksreceived += 1
                self.worked = True
                print(caster.name + " dealt 3 damage to " + target.name + " using double edged sword")
                print(caster.name + " dealt 2 damage to " + caster.name + " because of double edged sword")

        elif self.name == "Stand Tall":
            caster.abilitylastused = "Stand Tall"
            caster.abilitylasttarget = [player.name for player in targets]
            if caster.attacksreceived >= 2:
                for target in targets:
                    log.append([caster, 8, target])
                    caster.EXP += 8
                    target.EXP += 8
                    target.HP -= 8
                    self.worked = True
                    print(caster.name + " dealt 8 damage to " + target.name + " using Stand Tall")
            
        elif self.name == "Uncertain Footing":
            caster.abilitylastused = "Uncertain Footing"
            caster.abilitylasttarget = [player.name for player in targets]
            if not caster.damaged:
                for target in targets:
                    log.append([caster, 8, target])
                    caster.EXP += 8
                    target.EXP += 8
                    target.HP -= 8
                    self.worked = True
                    print(caster.name + " dealt 8 damage to " + target.name + " using Uncertain Footing")

        elif self.name == "QuickPoke":
            caster.abilitylastused = "QuickPoke"
            caster.abilitylasttarget = [p.name for p in targets]
##            for player in player:
##                if player == self.caster:
##                    pass
##                else:
##                    caster.abilitylasttarget.append(player.name)
            caster.dealtdamage = True
            for target in players:
                if target == caster:
                    pass
                else:
                    log.append([caster, 1, target])
                    target.EXP += 1
                    target.HP -= 1
                    caster.EXP += 1
                    target.damaged = True
                    target.attacksreceived += 1
                    self.worked = True
                    print(caster.name + " dealt 1 damage to " + target.name + " using QuickPoke")
                
        elif self.name == "chill":
            caster.abilitylastused = "chill"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.HP += 3
            self.worked = True
            print(caster.name + " regained 3 damage using Chill")

        elif self.name == "Spear Throw":
            caster.abilitylastused = "Spear Trhow"
            caster.abilitylasttarget = [player.name for player in targets]
            a = R.randint(1, 100)
            if a > 55:
                print(caster.name + " missed the Spear Throw")
            else:
                caster.dealtdamage = True
                b=R.randint(1,12)
                c=R.randint(1,12)
                d=R.randint(1,12)
                e = b + c + d
                for target in targets:
                    log.append([caster, e, target])
                    caster.EXP += e
                    target.HP -= e
                    target.EXP += e
                    target.damaged = True
                    target.attacksreceived += 1
                    self.worked = True
                    print(caster.name + " dealt " + str(e) +" damage to " + target.name + " using Spear Throw")

        elif self.name == "Kick":
            caster.abilitylastused = "Kick"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.dealtdamage = True
            a = R.randint(1,10)
            b = R.randint(1,10)
            c = a + b
            for target in targets:
                log.append([caster, c, target])
                caster.EXP += c
                target.EXP += c
                target.HP -= c
                target.damaged = True
                target.attacksreceived += 1
                self.worked = True
                print(caster.name + " dealt " + str(c) +" damage to " + target.name + " using Kick")

        elif self.name == "Punch":
            caster.abilitylastused = "Punch"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.dealtdamage = True
            for target in targets:
                log.append([caster, 9, target])
                caster.EXP += 9
                target.EXP += 9
                target.HP -= 9
                target.damaged = True
                target.attacksreceived += 1
                self.worked = True
                print(caster.name + " dealt 9 damage to " + target.name + " using Punch")

        elif self.name == "Blood Drain":
            caster.abilitylastused = "Blood Drain"
            caster.abilitylasttarget = [player.name for player in targets]
            d = R.randint(1,100)
            if d <= 75:
                caster.dealtdamage = True
                a = R.randint(1,8)
                b = R.randint(1,8)
                c = a + b
                for target in targets:
                    log.append([caster, c, target])
                    caster.EXP += c
                    target.EXP += c
                    target.HP -= c
                    caster.HP += c
                    target.damaged = True
                    target.attacksreceived += 1
                    self.worked = True
                    print(caster.name + " dealt " + str(c) +" damage to " + target.name + " using Blood Drain")
            else:
                print(caster.name + " missed Blood Drain")

        elif self.name == "Headbutt":
            caster.abilitylastused = "Headbutt"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.dealtdamage = True
            d = R.randint(1,100)
            if d <= 10:
                caster.conditions.append(condition("Paralyzed", caster, "chooseability", 1))
                print(caster.name + " paralyzed himself with Headbutt")
            for target in targets:
                a = R.randint(1,12)
                b = R.randint(1,12)
                c = a + b
                log.append([caster, c, target])
                caster.EXP += c
                target.EXP += c
                target.HP -= c
                target.damaged = True
                target.attacksreceived += 1
                self.worked = True
                print(caster.name + " dealt " + str(c) + " damage to " + target.name + " using Headbutt. d = " + str(d))
                
        elif self.name == "On The Edge":
            caster.abilitylastused = "On The Edge"
            caster.abilitylasttarget = [player.name for player in targets]
            a = 0
            b = 0
            for player in players:
                if player == caster:
                    pass
                else:
                    if player.ability.abilitytype == "Offensive":
                        a += 1
                    if caster in player.target:
                        b += 1
            
            if a == b and a > 0:
                for target in targets:
                    log.append([caster, 30, target])
                    caster.EXP += 30
                    target.EXP += 30
                    target.HP -= 30
                    self.worked = True
                    target.damaged = True
                    target.attacksreceived += 1
                    print(caster.name + " dealt 30 damage to " + target.name + " using On The Edge")

        
        elif self.name == "Everyone... GET IN HERE!":
            caster.abilitylastused = "Everyone... GET IN HERE!"
            caster.abilitylasttarget = [player.name for player in targets]
            a = 0
            for p in players: #calcular quantos ataques te tao a dar target
                if p == caster:
                    pass
                elif (caster in p.target) and p.ability.abilitytype == "Offensive":
                    a = a + 1
                    
            for target in targets:
                n = 0
                for i in range(a):
                    b = R.randint(1,15)
                    n = n + b
                log.append([caster, n, target])
                caster.EXP += n
                target.EXP += n
                target.HP -= n
                self.worked = True
                target.damaged = True
                target.attacksreceived += 1
                print(caster.name + " dealt " + str(n) + " damage to " + target.name + " using Everyone... GET IN HERE!")

        elif self.name == "From The Shadows":
            caster.abilitylastused = "From The Shadows"
            caster.abilitylasttarget = [player.name for player in targets]
            a = 0
            for p in players: #verificar quantas pessoas te deram target:
                if p == caster:
                    pass
                elif caster in p.target:
                    a = a + 1
            if a == 0:
                for target in targets:
                    n = 0
                    for i in range(6):
                        b = R.randint(1,6)
                        n = n + b
                    log.append([caster, n, target])
                    caster.EXP += n
                    target.EXP += n
                    target.HP -= n
                    self.worked = True
                    target.damaged = True
                    target.attacksreceived += 1
                    print(caster.name + " dealt " + str(n) + " damage to " + target.name + " using From The Shadows")

        elif self.name == "Unleash The Power":
            caster.abilitylastused = "Unleash The Power"
            caster.abilitylasttarget = [player.name for player in targets]
            if  not (self.name in [i[0] for i in caster.abilitiesinchannel]): #verificar se o player ja esta a dar channel à habilidade
                caster.abilitiesinchannel.append([self.name, self.channel - 1, True])
                #este "True" é verdadeiro ou falso consuante esta habilidade foi usada esta ronda, visto que se a habilidade channel nao for usada uma ronda, entao o channel para.
                print(caster.name + " began channeling " + self.name + " for 4 rounds")
                self.worked = True
            else: #a é o indice das habilidades que estao em channel que é o desta habilidade
                a = [i[0] == "Unleash The Power" for i in caster.abilitiesinchannel].index(True)
                if caster.abilitiesinchannel[a][1] == 1: #se o channel chegou ao fim, a habilidade atua
                    caster.abilitiesinchannel[a][1] -= 1
                    b = R.randint(1,14)
                    c = R.randint(1,14)
                    d = R.randint(1,14)
                    e = R.randint(1,14)
                    f = b + c + d + e
                    caster.abilitiesincooldown.append(["Unleash The Power", 3 + 1])
                    for t in targets:
                        t.EXP += f
                        t.HP -= f
                        caster.EXP += f
                        self.worked = True
                        t.damaged = True
                        t.attacksreceived += 1
                        log.append([caster, f, t])
                        print(caster.name + " dealt " + str(f) + " damage to " + t.name + " using Unleash The Power")
                else:
                    caster.abilitiesinchannel[a][1] -= 1
                    caster.abilitiesinchannel[a][2] = True
                    self.worked = True
                    print("Only " + str(caster.abilitiesinchannel[a][1]) + " turns left until " + caster.name + " Unleashes The Power")
                    
        elif self.name == "Refreshing Waters":
            caster.abilitylastused = "Refreshing Waters"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.HP += 12
            self.worked = True
            print(caster.name + " regained 12 damage using Refreshing Waters")

        elif self.name == "Rock Solid":
            caster.abilitylastused = "Rock Solid"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.conditions.append(condition("Rock Solid", caster, 1, 1))
            self.worked = True
            caster.abilitiesincooldown.append(["Rock Solid", 5 + 1])

        elif self.name == "Regenerate":
            caster.abilitylastused = "Regenerate"
            caster.abilitylasttarget = [player.name for player in targets]
            a = R.randint(1,10)
            caster.conditions.append(condition("Regenerate", caster, 1, a))
            self.worked = True
            print(caster.name + " will regenerate 3 HP per turn for " + str(a) + " turns")

        elif self.name == "Fight Stance":
            caster.abilitylastused = "Fight Stance"
            caster.abilitylasttarget = [player.name for player in targets]
            a = R.randint(1,6)
            caster.conditions.append(condition("Fight Stance", caster, 3, a + 1))
            self.worked = True
            print(caster.name + " will deal 7 more damage for " + str(a) + " turns because of Fight Stance")

        elif self.name == "Limitless":
            caster.abilitylastused = "Limitless"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.conditions.append(condition("Limitless", caster, 3, 1 + 1))
            self.worked = True
            caster.abilitiesincooldown.append(["Limitless", 999])
            #self.cooldown = 999
            print(caster.name + " will deal double damage next turn because of Limitless")

        elif self.name == "Lullaby":
            caster.abilitylastused = "Lullaby"
            caster.abilitylasttarget = [player.name for player in targets]
            print(caster.name + " sang a Lullaby")
            caster.abilitiesincooldown.append(["Lullaby", 5 + 1])
            #self.cooldown = 5 + 1
            for player in players:
                if player == caster:
                    pass
                else:
                    a = R.randint(1,2)
                    if a == 1:
                        player.conditions.append(condition("Asleep", player, "chooseability", 5))
                        print(caster.name + " put " + player.name + " to Sleep. ")

        elif self.name == "Intimidate":
            caster.abilitylastused = "Intimidate"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.abilitiesincooldown.append(["Intimidate", 1 + 1])
            a = R.randint(1,6)
            for player in players:
                if player == caster:
                    pass
                else:
                    player.conditions.append(condition("Intimidated", player, 3, a + 1))
                    print(caster.name + " intimidated " + player.name + " for " + str(a) + " rounds ")
            
        elif self.name == "teste":
            caster.abilitylastused = "teste"
            caster.abilitylasttarget = [player.name for player in targets]
            caster.conditions.append(condition("teste", caster, 3, 4))


        elif self.name == "teste2":
            caster.abilitylastused = "teste2"
            caster.abilitylasttarget = [player.name for player in targets]
            for target in targets:
                target.conditions.append(condition("Paralyzed", target, "chooseability", 1))
                    
        elif self.name == "passed":
            caster.abilitylastused = "passed"
            caster.abilitylasttarget = []
            self.worked = True
            print(caster.name + " did nothing.")
            pass
#______________________________________________________________________________________________________________________________________________________________________

#fonts:
fonttime = pygame.font.SysFont("comicsans", 50, True)
fontA = pygame.font.SysFont("mayence", 30, False, True)
fontHP = pygame.font.SysFont("comicsans",20 ,False ,True)
fontend = pygame.font.SysFont("mayence", 180, True)

#texts:
#texttackle = fontA.render("Tackle", 1, (0,0,0))
#textchoosetarget = fonttime.render("choose target(s)!", 1, (255,0,0))
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
abilities[0].append(ability("Tackle",0, 1, False, 2, True, "Offensive"))
abilities[0].append(ability("Double Edged Sword",0, 1, False, 2, True, "Offensive"))
abilities[0].append(ability("chill",0, 0, True, 2, False, "Defensive"))

abilities[1].append(ability("Uncertain Footing",1, 1, False, 3, True, "Offensive"))
abilities[1].append(ability("Stand Tall",1, 1, False, 3, True, "Offensive"))
abilities[1].append(ability("QuickPoke",1, 3, False, 1, True, "Offensive"))


#abilities[1].append(ability("teste", 1, 0, True, 3, False))
#abilities[1].append(ability("teste2", 1, 2, True, 3, False))

abilities[2][0].append(ability("Spear Throw",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("Kick",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("Punch",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("On The Edge",2, 1,False, 3, True, "Offensive"))
abilities[2][0].append(ability("Blood Drain",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("Headbutt",2, 1,False, 2, True, "Offensive"))
abilities[2][0].append(ability("Everyone... GET IN HERE!",2, 1, False, 3, True, "Offensive"))
abilities[2][0].append(ability("From The Shadows" ,2, 1, False, 3, True, "Offensive"))
abilities[2][0].append(ability("Unleash The Power" ,2, 2, False, 2, True, "Offensive", cooldown = 2, channel = 4))


abilities[2][1].append(ability("Rock Solid",2, 0,True, 1, False, "Defensive", cooldown = 5))
abilities[2][1].append(ability("Refreshing Waters",2, 0,True, 2, False, "Defensive"))
abilities[2][1].append(ability("Regenerate",2, 0,True, 3, False, "Defensive"))

abilities[2][2].append(ability("Lullaby",2, 3,False, 3, False, "Utility", cooldown = 5))
abilities[2][2].append(ability("Fight Stance",2, 0,True, 3, False, "Utility"))
abilities[2][2].append(ability("Unleash the Chains",2, 0,True, 3, False, "Utility"))
abilities[2][2].append(ability("Limitless",2, 0,True, 3, False, "Utility", cooldown = 999))
abilities[2][2].append(ability("Intimidate",2, 0,False, 4, False, "Utility", cooldown = 1))
#______________________________________________________________________________________________________________________________________________________________________






roundphase = chooseability(1)
print("round: 1")

#______________________________________________________________________________________________________________________________________________________________________

#main loop
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #nao sei como ver se se clicou no lado esquerdo ou direito do rato... o lado esquerdo é 1 e o lado esquerdo é 3
                
                roundphase.receiveevent(event)
                
        if event.type == pygame.KEYDOWN:
                
                
            if event.key == pygame.K_DELETE:
                run = False
            elif event.key == pygame.K_g:
                roundphase.gainabilityforfree(craos)
            elif event.key == pygame.K_p:
                for player in players:
                    print(player.name)
            elif event.key == pygame.K_n:
                for npc in npcs:
                    print(npc.name)
            elif event.key == pygame.K_a:
                print("clicaste a para ver as habilidades de toda a gente.")
                for player in players:
                    print(player.name)
                    for a in player.abilities:
                        print(a.name)
                    print()
            elif event.key == pygame.K_l:
                for i in log:
                    print(str(i))


    roundphase.clock()
    roundphase.draw()
    roundphase.effect()

pygame.quit()
